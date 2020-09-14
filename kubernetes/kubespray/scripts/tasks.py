#!/usr/bin/env python

import os
import pip
from tempfile import NamedTemporaryFile

from fabric2 import task

try:
    import yaml
except ImportError:
    pip.main(['install', 'pyyaml'])
    import yaml

from cloudify import manager
from cloudify import ctx
from cloudify.exceptions import (RecoverableError, NonRecoverableError)

cfy_client = manager.get_rest_client()

KUBE_PATH = '/home/{0}/.kube/config'
MASTER_KUBE_PATH = '/etc/kubernetes/admin.conf'


def create_secret(key, val):
    cfy_client.secrets.create(
        key=key,
        value=val,
        update_if_exists=True)


def handle_fabric_response(fabric_response):
    if not fabric_response:
        raise NonRecoverableError('Unknown error when trying to run remote '
                                  'command')

    if fabric_response.failed:
        err_msg = '{0} failed with error: {1}'.format(
            fabric_response.command,
            fabric_response.stderr)
        ctx.logger.error(err_msg)
        raise NonRecoverableError(err_msg)

    success_msg = 'Running command: {0} successfully {1}'.format(
        fabric_response.command, fabric_response.stdout)

    ctx.logger.info(success_msg)


def create_cluster_secrets(cluster, rp):
    name = cluster.get('name')
    cluster_config = cluster.get('cluster', {})
    rp['kubernetes-cluster-name'] = name
    rp['kubernetes-server'] = cluster_config.get('server')
    create_secret('kubernetes-cluster-name', name)
    create_secret('kubernetes-server', cluster_config.get('server'))
    secret_name = '{0}-certificate-authority-data'.format(name)
    certificate_authority_content = cluster_config.get(
        'certificate-authority-data')
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


@task
def setup_kubectl(connection, username):
    kube_config_path = KUBE_PATH.format(username)
    connection.run('mkdir {0}'.format(os.path.dirname(kube_config_path)))
    connection.sudo('cp {0} {1}'.format(MASTER_KUBE_PATH, kube_config_path))
    connection.sudo('chown {0} {1}'.format(username, kube_config_path))
    connection.sudo('chmod 755 {0}'.format(kube_config_path))


def get_config_content(filename):
    with open(filename, 'r') as outfile:
        try:
            return yaml.load(outfile)
        except yaml.YAMLError as e:
            raise RecoverableError(
                'Unable to read file: {0}: {1}'.format(filename, str(e)))


@task
def setup_secrets(connection):
    f = NamedTemporaryFile()
    connection.sudo(
        'chmod 775 {kubeconfig}'.format(kubeconfig=MASTER_KUBE_PATH))
    connection.get(MASTER_KUBE_PATH, f.name)
    rp = ctx.target.instance.runtime_properties
    rp['configuration_file_content'] = get_config_content(f.name)
    for cluster in rp['configuration_file_content'].get('clusters'):
        create_cluster_secrets(cluster, rp)
    for user in rp['configuration_file_content'].get('users'):
        create_user_secrets(user, rp)


@task
def kubectl_apply(connection, username, resource):
    f = NamedTemporaryFile()
    kube_config_path = KUBE_PATH.format(username)
    ctx.download_resource('resources/{0}'.format(resource), f.name)
    connection.put(f.name, '/home/{0}/{1}'.format(username, resource))
    connection.run('kubectl apply --namespace=kube-system -f {0}/{1}'.format(
        os.path.dirname(
            os.path.dirname(kube_config_path)
        ), resource
    ), env={"KUBE_CONFIG": kube_config_path})


@task
def setup_helm(connection, username, resource):
    """
    This task will install.setup helm inside K8S cluster and will init the
    tiller server
    """

    temp_file = NamedTemporaryFile()
    # Download helm script file to the home directory
    helm_script_path = '/home/{0}/{1}'.format(username, resource)
    ctx.download_resource('scripts/{0}'.format(resource), temp_file.name)

    # Copy file to the home directory
    ctx.logger.debug(
        'Copy {0} to {1}'.format(temp_file.name, helm_script_path)
    )
    connection.put(temp_file.name, helm_script_path)

    # Change owner for the helm script file
    ctx.logger.debug(
        'Change file {0} owner to {1}'.format(helm_script_path, username)
    )
    connection.sudo('chown {0} {1}'.format(username, helm_script_path))

    # Update Permissions
    ctx.logger.debug(
        'Change file {0} permission to 700'.format(helm_script_path)
    )
    connection.sudo('chmod 700 {0}'.format(helm_script_path))

    # Install Helm client
    ctx.logger.debug(
        'Install helm client using script file {0}'.format(
            helm_script_path)
    )
    response = connection.run('bash {0}'.format(helm_script_path))
    handle_fabric_response(response)

    # Initialize helm and install tiller server
    ctx.logger.debug('Initialize helm and install tiller server')
    response = connection.run('helm init')
    handle_fabric_response(response)
