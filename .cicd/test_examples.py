########
# Copyright (c) 2014-2019 Cloudify Platform Ltd. All rights reserved
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


import os
import base64
import pytest

from ecosystem_tests.dorkl import (
    blueprints_upload,
    basic_blueprint_test,
    logging, cleanup_on_failure, prepare_test, docker_exec
)

from __init__ import blueprint_list, get_cloudify_version, VersionsException

OS_VERSION = '3.2.12'
UT_VERSION = '1.21.0'
TF_VERSION = '0.13.1'

TF_WAGON = 'http://repository.cloudifysource.org/cloudify/wagons/' \
           'cloudify-terraform-plugin/{v}/cloudify_terraform_plugin' \
           '-{v}-py27-none-linux_x86_64-centos-Core.wgn'.format(v=TF_VERSION)
TF_PLUGIN = 'http://www.getcloudify.org/spec/terraform-plugin/' \
            '{v}/plugin.yaml'.format(v=TF_VERSION)
OS_WAGON = 'http://repository.cloudifysource.org/cloudify/wagons/' \
           'cloudify-openstack-plugin/{v}/cloudify_openstack_plugin' \
           '-{v}-py27-none-linux_x86_64-centos-Core.wgn'.format(v=OS_VERSION)
OS_PLUGIN = 'http://www.getcloudify.org/spec/openstack-plugin/' \
            '{v}/plugin.yaml'.format(v=OS_VERSION)
UT_WAGON = 'http://repository.cloudifysource.org/cloudify/wagons/' \
           'cloudify-utilities-plugin/{v}/cloudify_utilities_plugin' \
           '-{v}-py27-none-linux_x86_64-centos-Core.wgn'.format(v=UT_VERSION)
UT_PLUGIN = 'http://www.getcloudify.org/spec/utilities-plugin/' \
            '{v}/plugin.yaml'.format(v=UT_VERSION)

PLUGINS_TO_UPLOAD = [(OS_WAGON, OS_PLUGIN), (TF_WAGON, TF_PLUGIN),
                     (UT_WAGON, UT_PLUGIN)]

SECRETS = {
    'aws_access_key_id': False,
    'aws_secret_access_key': False,
    'aws_region_name': False,
    'ec2_region_endpoint': False,
    'azure_subscription_id': False,
    'azure_tenant_id': False,
    'azure_client_id': False,
    'azure_location': False,
    'openstack_username': False,
    'openstack_password': False,
    'openstack_tenant_name': False,
    'openstack_auth_url': False,
    'openstack_region': False,
    'base_image_id': False,
    'base_flavor_id': False,
    'gcp_credentials': True
}

prepare_test(plugins=PLUGINS_TO_UPLOAD, secrets=SECRETS)

virtual_machine_list = [b for b in blueprint_list if 'virtual-machine' in b]
getting_started_list = [b for b in blueprint_list if 'getting-started' in b]


def get_dirname_and_infra_name(blueprint_path):
    dirname_param = os.path.dirname(blueprint_path).split('/')[-1:][0]
    infra_name = os.path.basename(blueprint_path).split('.yaml')[0]
    return dirname_param, infra_name


def blueprint_id_filter(blueprint_path):
    # For the db-lb-app, we need a blueprint named 'infrastructure'.
    # So this makes sure that the first one that gets uploaded (aws)
    # will be the reference.
    # TODO: Add to supported examples.json desired blueprint name.
    dirname_param, infra_name = get_dirname_and_infra_name(blueprint_path)
    if dirname_param == 'infrastructure' and infra_name == 'azure':
        blueprint_id = '{0}'.format(dirname_param)
    elif dirname_param == 'infrastructure' and infra_name == 'aws':
        blueprint_id = 'public-cloud-vm'
    elif dirname_param == 'infrastructure' and infra_name == 'openstack':
        blueprint_id = 'private-cloud-vm'
    else:
        blueprint_id = '{0}-{1}'.format(
            dirname_param,
            infra_name)
    return blueprint_id


def blueprint_filter(blueprint_name, blueprint_path):
    return blueprint_name in blueprint_path


@pytest.fixture(scope='function', params=blueprint_list)
def upload_blueprints_for_validation(request):
    blueprints_upload(request.param, blueprint_id_filter(request.param))


@pytest.fixture(scope='function', params=virtual_machine_list)
def basic_blueprint_test_with_getting_started_filter(request):
    logging.info('Testing getting started with: {0}.'.format(request.param))
    _, infra_name = get_dirname_and_infra_name(request.param)
    blueprints_upload(request.param, 'infra-{0}'.format(infra_name))
    for blueprint_path in getting_started_list:
        blueprint_id = '{0}-{1}'.format(
            blueprint_id_filter(blueprint_path), infra_name)
        logging.info('Executing getting started test: {0}:{1}.'.format(
            blueprint_id,
            infra_name))
        try:
            basic_blueprint_test(
                blueprint_path,
                blueprint_id,
                inputs='infra_name={0} -i infra_exists=true'.format(
                    infra_name))
        except:
            cleanup_on_failure(blueprint_id)
            raise


def test_blueprint_validation(upload_blueprints_for_validation):
    """All blueprints must pass DSL validation."""
    assert upload_blueprints_for_validation is None


def test_versions():
    """All blueprints in this branch should be the same Cloudify version.
    """
    try:
        assert get_cloudify_version() is not None
    except VersionsException as e:
        pytest.fail(
            "Failed to verify that branch "
            "versions are the same: {0}.".format(str(e)))


def test_getting_started(basic_blueprint_test_with_getting_started_filter):
    assert basic_blueprint_test_with_getting_started_filter is None
