# Note, this contains some advanced info.

import os
import sys
import subprocess
from requests import get
from urllib.request import urlopen

# Import Cloudify's context object.
# This provides several useful functions as well as allowing to pass
# contextual information of an application.
from cloudify import ctx


IS_WIN = os.name == 'nt'

# Get the port from the blueprint. We're running this script in the context of
# the `http_web_server` node so we can read its `port` property.
PORT = ctx.node.properties['port']
DEFAULT_IP = '<manager-ip>'
URL = 'http://{ip}:{port}'


def run_server():
    os.chdir('/opt/manager/resources/blueprints/{0}/{1}'.format(
        ctx.tenant_name,
        ctx.blueprint.id))
    server_module = ('SimpleHTTPServer' if sys.version_info < (3, 0)
                     else 'http.server')
    webserver_cmd = [sys.executable, '-m', server_module, str(PORT)]
    if not IS_WIN:
        webserver_cmd.insert(0, 'nohup')

    # The ctx object provides a built in logger.
    ctx.logger.info('Running WebServer locally on port: {0}'.format(PORT))
    # emulating /dev/null
    with open(os.devnull, 'wb') as dn:
        process = subprocess.Popen(webserver_cmd, stdout=dn, stderr=dn)
    return process.pid


def set_pid(pid):
    ctx.logger.info('Setting `pid` runtime property: {0}'.format(pid))
    # We can set runtime information in our context object which
    # can later be read somewhere in the context of the instance.
    # For instance, we want to save the `pid` here so that when we
    # run `uninstall.py`, we can destroy the process.
    ctx.instance.runtime_properties['pid'] = pid


def get_host_ip():
    host_ip = _find_ip()
    ctx.logger.info('The application endpoint is '
                    '{0}'.format(URL.format(ip=host_ip, port=PORT)))
    if host_ip == DEFAULT_IP:
        ctx.logger.info('Please replace {0} with the host IP as you know '
                        'it'.format(DEFAULT_IP))
    ctx.instance.runtime_properties['ip'] = host_ip


def _find_ip():
    ctx.logger.info('Trying to find the host IP')
    try:
        if _is_inside_docker():
            raw_ip = subprocess.check_output(['hostname', '-i'])
            ip = raw_ip.decode('utf-8').rstrip()
        else:
            ip = get('https://api.ipify.org').text
            url = URL.format(ip=ip, port=PORT)
            urlopen(url, timeout=1)  # Trying to open a connection to the URL
        return ip
    except Exception:
        ctx.logger.info('Could not find the host IP.')
        return DEFAULT_IP


def _is_inside_docker():
    """ Check whether running inside a docker container"""
    with open('/proc/1/cgroup', 'rt') as f:
        return 'docker' in f.read()


pid = run_server()
set_pid(pid)
get_host_ip()
