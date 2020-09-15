#!/usr/bin/env python
#
# Copyright (c) 2018 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
import subprocess

from fabric2 import task

from cloudify import ctx
from cloudify.manager import get_rest_client
from cloudify.exceptions import NonRecoverableError
from cloudify.utils import exception_to_error_cause


def execute_command(_command):
    ctx.logger.info('command {0}.'.format(_command))

    process = subprocess.Popen([_command], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)

    output, error = process.communicate()

    if process.returncode:
        ctx.logger.error('Running `{0}` returns error.'.format(_command))
        return False

    ctx.logger.info('Command output: {0} '.format(output.strip()))

    ctx.logger.info('Command error: {0} '.format(error))

    ctx.logger.info('Command process return code: {0} '
                    ''.format(process.returncode))

    return output


def generate_traceback_exception():
    _, exc_value, exc_traceback = sys.exc_info()
    response = exception_to_error_cause(exc_value, exc_traceback)
    ctx.logger.error(
        'Error traceback {0} with message {1}'.format(
            response['traceback'], response['message']))


def generate_token_and_port(connection):
    # Command to get the service account name
    service_account_cmd_1 = \
        "kubectl -n kube-system get secret" \
        " | grep admin-user | awk \'{print $1}\'"

    # Execute the command and fetch the service account name
    output = connection.run(service_account_cmd_1)

    # Retry in case the command fail
    if not output:
        raise NonRecoverableError('Failed to get the service account')

    print(dir(output))
    # Command to get the associated bearer token with service account
    service_account_cmd_2 = \
        "kubectl -n kube-system describe secret {0}" \
        " | grep -E '^token' | cut -f2 -d':' | tr -d '\t'".format(
            output.stdout.strip())

    # Execute the command and fetch the token associated with account
    bearer_token = connection.run(service_account_cmd_2)

    # Retry in case the command fail
    if not bearer_token:
        raise NonRecoverableError('Failed to get the bearer token')

    # Command to get the exposed port on which kubernetes ui is running
    exposed_port_cmd = \
        "kubectl -n kube-system get service kubernetes-dashboard" \
        " | awk 'FNR == 2 {print $5}' | cut -f2 -d':' | cut -f1 -d '/'"

    # Execute the command and get the output
    port = connection.run(exposed_port_cmd)

    # Retry in case the command fail
    if not port:
        raise NonRecoverableError(
            'Failed to get the kubernetes dashboard port'
        )

    # Set the generated token and set it as run time properties for  instance
    token = bearer_token.stdout.strip()
    client = get_rest_client()
    client.secrets.create('kubernetes_token', token, update_if_exists=True)
    ctx.instance.runtime_properties['bearer_token'] = token
    # Set the exposed port and set it as run time properties for instance
    ctx.instance.runtime_properties['dashboard_port'] = port.stdout.strip()


@task
def setup_dashboard_access(connection):
    try:
        generate_token_and_port(connection)
    except Exception:
        generate_traceback_exception()
        raise SystemExit('Failed To setup dashboard access')
