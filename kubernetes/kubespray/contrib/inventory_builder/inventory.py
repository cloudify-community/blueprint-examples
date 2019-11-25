#!/usr/bin/env python3
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Usage: inventory.py ip1 [ip2 ...]
# Examples: inventory.py 10.10.1.3 10.10.1.4 10.10.1.5
#
# Advanced usage:
# Add another host after initial creation: inventory.py 10.10.1.5
# Add range of hosts: inventory.py 10.10.1.3-10.10.1.5
# Add hosts with different ip and access ip: inventory.py 10.0.0.1,192.168.10.1 10.0.0.2,192.168.10.2 10.0.0.3,192.168.10.3
# Delete a host: inventory.py -10.10.1.3
# Delete a host by id: inventory.py -node1
#
# Load a YAML or JSON file with inventory data: inventory.py load hosts.yaml
# YAML file should be in the following format:
#    group1:
#      host1:
#        ip: X.X.X.X
#        var: val
#    group2:
#      host2:
#        ip: X.X.X.X

from collections import OrderedDict
from ruamel.yaml import YAML

import os
import re
import sys

ROLES = ['all', 'kube-master', 'kube-node', 'etcd', 'k8s-cluster',
         'calico-rr']
PROTECTED_NAMES = ROLES
AVAILABLE_COMMANDS = ['help', 'print_cfg', 'print_ips', 'load']
_boolean_states = {'1': True, 'yes': True, 'true': True, 'on': True,
                   '0': False, 'no': False, 'false': False, 'off': False}
yaml = YAML()


def get_var_as_bool(name, default):
    value = os.environ.get(name, '')
    return _boolean_states.get(value.lower(), default)

# Configurable as shell vars start

CONFIG_FILE = os.environ.get("CONFIG_FILE", "./inventory/sample/hosts.yaml")
# Reconfigures cluster distribution at scale
SCALE_THRESHOLD = int(os.environ.get("SCALE_THRESHOLD", 50))
MASSIVE_SCALE_THRESHOLD = int(os.environ.get("SCALE_THRESHOLD", 200))

DEBUG = get_var_as_bool("DEBUG", True)
HOST_PREFIX = os.environ.get("HOST_PREFIX", "node")

# Configurable as shell vars end


class KubesprayInventory(object):

    def __init__(self, changed_hosts=None, config_file=None):
        self.config_file = config_file
        self.yaml_config = {}
        if self.config_file:
            try:
                self.hosts_file = open(config_file, 'r')
                self.yaml_config = yaml.load(self.hosts_file)
            except FileNotFoundError:
                pass

        if changed_hosts and changed_hosts[0] in AVAILABLE_COMMANDS:
            self.parse_command(changed_hosts[0], changed_hosts[1:])
            sys.exit(0)

        self.ensure_required_groups(ROLES)

        if changed_hosts:
            changed_hosts = self.range2ips(changed_hosts)
            self.hosts = self.build_hostnames(changed_hosts)
            self.purge_invalid_hosts(self.hosts.keys(), PROTECTED_NAMES)
            self.set_all(self.hosts)
            self.set_k8s_cluster()
            self.set_etcd(list(self.hosts.keys())[:3])
            if len(self.hosts) >= SCALE_THRESHOLD:
                self.set_kube_master(list(self.hosts.keys())[3:5])
            else:
                self.set_kube_master(list(self.hosts.keys())[:2])
            self.set_kube_node(self.hosts.keys())
            if len(self.hosts) >= SCALE_THRESHOLD:
                self.set_calico_rr(list(self.hosts.keys())[:3])
        else:  # Show help if no options
            self.show_help()
            sys.exit(0)

        self.write_config(self.config_file)

    def write_config(self, config_file):
        if config_file:
            with open(self.config_file, 'w') as f:
                yaml.dump(self.yaml_config, f)

        else:
            print("WARNING: Unable to save config. Make sure you set "
                  "CONFIG_FILE env var.")

    def debug(self, msg):
        if DEBUG:
            print("DEBUG: {0}".format(msg))

    def get_ip_from_opts(self, optstring):
        if 'ip' in optstring:
            return optstring['ip']
        else:
            raise ValueError("IP parameter not found in options")

    def ensure_required_groups(self, groups):
        for group in groups:
            if group == 'all':
                self.debug("Adding group {0}".format(group))
                if group not in self.yaml_config:
                    self.yaml_config = {'all':
                                        {'hosts': {},
                                         'vars':
                                         {'ansible_user': 'centos'},
                                         'children': {}}}
            else:
                self.debug("Adding group {0}".format(group))
                if group not in self.yaml_config['all']['children']:
                    self.yaml_config['all']['children'][group] = {'hosts': None}

    def get_host_id(self, host):
        '''Returns integer host ID (without padding) from a given hostname.'''
        try:
            short_hostname = host.split('.')[0]
            return int(re.findall("\d+$", short_hostname)[-1])
        except IndexError:
            raise ValueError("Host name must end in an integer")

    def build_hostnames(self, changed_hosts):
        existing_hosts = OrderedDict()
        highest_host_id = 0
        try:
            for host in self.yaml_config['all']['hosts']:
                existing_hosts[host] = self.yaml_config['all']['hosts'][host]
                host_id = self.get_host_id(host)
                if host_id > highest_host_id:
                    highest_host_id = host_id
        except Exception:
            pass

        # FIXME(mattymo): Fix condition where delete then add reuses highest id
        next_host_id = highest_host_id + 1

        all_hosts = existing_hosts.copy()
        for host in changed_hosts:
            if host[0] == "-":
                realhost = host[1:]
                if self.exists_hostname(all_hosts, realhost):
                    self.debug("Marked {0} for deletion.".format(realhost))
                    all_hosts.pop(realhost)
                elif self.exists_ip(all_hosts, realhost):
                    self.debug("Marked {0} for deletion.".format(realhost))
                    self.delete_host_by_ip(all_hosts, realhost)
            elif host[0].isdigit():
                if ',' in host:
                    ip, access_ip = host.split(',')
                else:
                    ip = host
                    access_ip = host
                if self.exists_hostname(all_hosts, host):
                    self.debug("Skipping existing host {0}.".format(host))
                    continue
                elif self.exists_ip(all_hosts, ip):
                    self.debug("Skipping existing host {0}.".format(ip))
                    continue

                next_host = "{0}{1}".format(HOST_PREFIX, next_host_id)
                next_host_id += 1
                all_hosts[next_host] = {'ansible_host': access_ip,
                                        'ip': ip,
                                        'access_ip': access_ip}
            elif host[0].isalpha():
                raise Exception("Adding hosts by hostname is not supported.")

        return all_hosts

    def range2ips(self, hosts):
        from ipaddress import ip_address
        reworked_hosts = []

        def ips(start_address, end_address):
            start = int(ip_address(start_address).packed.hex(), 16)
            end = int(ip_address(end_address).packed.hex(), 16)
            return [ip_address(ip).exploded for ip in range(start, end+1)]

        for host in hosts:
            if '-' in host and not host.startswith('-'):
                start, end = host.strip().split('-')
                try:
                    reworked_hosts.extend(ips(start, end))
                except ValueError:
                    raise Exception("Range of ip_addresses isn't valid")
            else:
                reworked_hosts.append(host)
        return reworked_hosts

    def exists_hostname(self, existing_hosts, hostname):
        return hostname in existing_hosts.keys()

    def exists_ip(self, existing_hosts, ip):
        for host_opts in existing_hosts.values():
            if ip == self.get_ip_from_opts(host_opts):
                return True
        return False

    def delete_host_by_ip(self, existing_hosts, ip):
        for hostname, host_opts in existing_hosts.items():
            if ip == self.get_ip_from_opts(host_opts):
                del existing_hosts[hostname]
                return
        raise ValueError("Unable to find host by IP: {0}".format(ip))

    def purge_invalid_hosts(self, hostnames, protected_names=[]):
        for role in self.yaml_config['all']['children']:
            if role != 'k8s-cluster' and self.yaml_config['all']['children'][role]['hosts']:
                all_hosts = self.yaml_config['all']['children'][role]['hosts'].copy()
                for host in all_hosts.keys():
                    if host not in hostnames and host not in protected_names:
                        self.debug("Host {0} removed from role {1}".format(host, role))
                        del self.yaml_config['all']['children'][role]['hosts'][host]
        # purge from all
        if self.yaml_config['all']['hosts']:
            all_hosts = self.yaml_config['all']['hosts'].copy()
            for host in all_hosts.keys():
                if host not in hostnames and host not in protected_names:
                    self.debug("Host {0} removed from role all".format(host))
                    del self.yaml_config['all']['hosts'][host]

    def add_host_to_group(self, group, host, opts=""):
        self.debug("adding host {0} to group {1}".format(host, group))
        if group == 'all':
            if self.yaml_config['all']['hosts'] is None:
                self.yaml_config['all']['hosts'] = {host: None}
            self.yaml_config['all']['hosts'][host] = opts
        elif group != 'k8s-cluster:children':
            if self.yaml_config['all']['children'][group]['hosts'] is None:
                self.yaml_config['all']['children'][group]['hosts'] = {host: None}
            else:
                self.yaml_config['all']['children'][group]['hosts'][host] = None

    def set_kube_master(self, hosts):
        for host in hosts:
            self.add_host_to_group('kube-master', host)

    def set_all(self, hosts):
        for host, opts in hosts.items():
            self.add_host_to_group('all', host, opts)

    def set_k8s_cluster(self):
        self.yaml_config['all']['children']['k8s-cluster'] = {'children':
                                                              {'kube-master': None,
                                                               'kube-node': None}}

    def set_calico_rr(self, hosts):
        for host in hosts:
            if host in self.yaml_config['all']['children']['kube-master']:
                    self.debug("Not adding {0} to calico-rr group because it "
                               "conflicts with kube-master group".format(host))
                    continue
            if host in self.yaml_config['all']['children']['kube-node']:
                    self.debug("Not adding {0} to calico-rr group because it "
                               "conflicts with kube-node group".format(host))
                    continue
            self.add_host_to_group('calico-rr', host)

    def set_kube_node(self, hosts):
        for host in hosts:
            if len(self.yaml_config['all']['hosts']) >= SCALE_THRESHOLD:
                if host in self.yaml_config['all']['children']['etcd']['hosts']:
                    self.debug("Not adding {0} to kube-node group because of "
                               "scale deployment and host is in etcd "
                               "group.".format(host))
                    continue
            if len(self.yaml_config['all']['hosts']) >= MASSIVE_SCALE_THRESHOLD:
                if host in self.yaml_config['all']['children']['kube-master']['hosts']:
                    self.debug("Not adding {0} to kube-node group because of "
                               "scale deployment and host is in kube-master "
                               "group.".format(host))
                    continue
            self.add_host_to_group('kube-node', host)

    def set_etcd(self, hosts):
        for host in hosts:
            self.add_host_to_group('etcd', host)

    def load_file(self, files=None):
        '''Directly loads JSON to inventory.'''

        if not files:
            raise Exception("No input file specified.")

        import json

        for filename in list(files):
            # Try JSON
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
            except ValueError:
                raise Exception("Cannot read %s as JSON, or CSV", filename)

            self.ensure_required_groups(ROLES)
            self.set_k8s_cluster()
            for group, hosts in data.items():
                self.ensure_required_groups([group])
                for host, opts in hosts.items():
                    optstring = {'ansible_host': opts['ip'],
                                 'ip': opts['ip'],
                                 'access_ip': opts['ip']}
                    self.add_host_to_group('all', host, optstring)
                    self.add_host_to_group(group, host)
            self.write_config(self.config_file)

    def parse_command(self, command, args=None):
        if command == 'help':
            self.show_help()
        elif command == 'print_cfg':
            self.print_config()
        elif command == 'print_ips':
            self.print_ips()
        elif command == 'load':
            self.load_file(args)
        else:
            raise Exception("Invalid command specified.")

    def show_help(self):
        help_text = '''Usage: inventory.py ip1 [ip2 ...]
Examples: inventory.py 10.10.1.3 10.10.1.4 10.10.1.5

Available commands:
help - Display this message
print_cfg - Write inventory file to stdout
print_ips - Write a space-delimited list of IPs from "all" group

Advanced usage:
Add another host after initial creation: inventory.py 10.10.1.5
Add range of hosts: inventory.py 10.10.1.3-10.10.1.5
Add hosts with different ip and access ip: inventory.py 10.0.0.1,192.168.10.1 10.0.0.2,192.168.10.2 10.0.0.3,192.168.10.3
Delete a host: inventory.py -10.10.1.3
Delete a host by id: inventory.py -node1

Configurable env vars:
DEBUG                   Enable debug printing. Default: True
CONFIG_FILE             File to write config to Default: ./inventory/sample/hosts.yaml
HOST_PREFIX             Host prefix for generated hosts. Default: node
SCALE_THRESHOLD         Separate ETCD role if # of nodes >= 50
MASSIVE_SCALE_THRESHOLD Separate K8s master and ETCD if # of nodes >= 200
'''
        print(help_text)

    def print_config(self):
        yaml.dump(self.yaml_config, sys.stdout)

    def print_ips(self):
        ips = []
        for host, opts in self.yaml_config['all']['hosts'].items():
            ips.append(self.get_ip_from_opts(opts))
        print(' '.join(ips))


def main(argv=None):
    if not argv:
        argv = sys.argv[1:]
    KubesprayInventory(argv, CONFIG_FILE)

if __name__ == "__main__":
    sys.exit(main())
