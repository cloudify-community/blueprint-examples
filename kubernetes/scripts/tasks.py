#!/usr/bin/env python

import os
import pip
from tempfile import NamedTemporaryFile

try:
    import yaml
except ImportError:
    pip.main(['install', 'pyyaml'])
    import yaml

from cloudify import manager
from cloudify import ctx
from cloudify.exceptions import RecoverableError

from fabric.api import sudo, get, put, shell_env, run

cfy_client = manager.get_rest_client()

KUBE_PATH = '/home/{0}/.kube/config'
MASTER_KUBE_PATH = '/etc/kubernetes/admin.conf'


def create_secret(key, val):
    cfy_client.secrets.create(
        key=key,
        value=val,
        update_if_exists=True)


def create_cluster_secrets(cluster, rp):
    name = cluster.get('name')
    cluster_config = cluster.get('cluster', {})
    rp['kubernetes-cluster-name'] = name
    rp['kubernetes-server'] = cluster_config.get('server')
    create_secret('kubernetes-cluster-name', name)
    create_secret('kubernetes-server', cluster_config.get('server'))
    secret_name = '{0}-certificate-authority-data'.format(name)
    certificate_authority_content = cluster_config.get('certificate-authority-data')
    create_secret(secret_name, certificate_authority_content)
    rp[secret_name] = certificate_authority_content


def create_user_secrets(user, rp):
    name = user.get('name')
    user_config = user.get('user', {})
    rp['kubernetes-username'] = name
    secret_name = '{0}-client-certificate-data'.format(name)
    certificate_content = user_config.get('client-certificate-data')
    create_secret(secret_name, certificate_content)
    rp[secret_name] = certificate_content
    del secret_name
    secret_name = '{0}-client-key-data'.format(name, user_config)
    key_content = user_config.get('client-key-data')
    create_secret(secret_name, key_content)
    rp[secret_name] = key_content
    del secret_name


def setup_kubectl(username):
    kube_config_path = KUBE_PATH.format(username)
    run('mkdir {0}'.format(os.path.dirname(kube_config_path)))
    sudo('cp {0} {1}'.format(MASTER_KUBE_PATH, kube_config_path))
    sudo('chown {0} {1}'.format(username, kube_config_path))
    sudo('chmod 755 {0}'.format(kube_config_path))


def get_config_content(filename):
    with open(filename, 'r') as outfile:
        try:
            return yaml.load(outfile)
        except yaml.YAMLError as e:
            raise RecoverableError(
                'Unable to read file: {0}: {1}'.format(filename, str(e)))


def setup_secrets():
    f = NamedTemporaryFile()
    get(MASTER_KUBE_PATH, f.name, use_sudo=True)
    rp = ctx.target.instance.runtime_properties
    rp['configuration_file_content'] = get_config_content(f.name)
    for cluster in rp['configuration_file_content'].get('clusters'):
        create_cluster_secrets(cluster, rp)
    for user in rp['configuration_file_content'].get('users'):
        create_user_secrets(user, rp)


def kubectl_apply(username, resource):
    f = NamedTemporaryFile()
    kube_config_path = KUBE_PATH.format(username)
    ctx.download_resource('resources/{0}'.format(resource), f.name)
    put(f.name, '/home/{0}/{1}'.format(username, resource))
    with shell_env(KUBE_CONFIG=kube_config_path):
        run('kubectl apply --namespace=kube-system -f {0}/{1}'.format(
            os.path.dirname(
                os.path.dirname(kube_config_path)
            ), resource
        ))
