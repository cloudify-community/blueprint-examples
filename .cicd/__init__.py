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
from urlparse import urlparse
from collections import OrderedDict
from json import load as load_json
from yaml import load as yaml_load, YAMLError

CWD = '/{0}'.format(
    '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[1:-1],))
SUPPORTED_EXAMPLES_FILE = os.path.join(CWD, '.cicd/supported_examples.json')


OS_VERSION = '3.2.15'
UT_VERSION = '1.21.0'
TF_VERSION = '0.13.2'
DK_VERSION = '2.0.1'
AN_VERSION = '2.9.1'

TF_WAGON = 'https://github.com/cloudify-cosmo/cloudify-terraform-plugin/' \
           'releases/download/{v}/cloudify_terraform_plugin-{v}-py27-none-' \
           'linux_x86_64-centos-Core.wgn'.format(v=TF_VERSION)
TF_PLUGIN = 'https://github.com/cloudify-cosmo/cloudify-terraform-plugin/' \
            'releases/download/{v}/plugin.yaml'.format(v=TF_VERSION)
OS_WAGON = 'https://github.com/cloudify-cosmo/cloudify-openstack-plugin/' \
           'releases/download/{v}/cloudify_openstack_plugin-{v}-py27-none-' \
           'linux_x86_64-centos-Core.wgn'.format(v=OS_VERSION)
OS_PLUGIN = 'https://github.com/cloudify-cosmo/' \
            'cloudify-openstack-plugin/releases/download/' \
            '{v}/plugin.yaml'.format(v=OS_VERSION)
UT_WAGON = 'http://repository.cloudifysource.org/cloudify/wagons/' \
           'cloudify-utilities-plugin/{v}/cloudify_utilities_plugin' \
           '-{v}-py27-none-linux_x86_64-centos-Core.wgn'.format(v=UT_VERSION)
UT_PLUGIN = 'http://www.getcloudify.org/spec/utilities-plugin/' \
            '{v}/plugin.yaml'.format(v=UT_VERSION)
DK_WAGON = 'https://github.com/cloudify-cosmo/cloudify-docker-plugin/' \
           'releases/download/{v}/cloudify_docker_plugin-{v}-py27-none-' \
           'linux_x86_64-centos-Core.wgn'.format(v=DK_VERSION)
DK_PLUGIN = 'https://github.com/cloudify-cosmo/cloudify-docker-plugin/' \
            'releases/download/{v}/plugin.yaml'.format(v=DK_VERSION)
AN_WAGON = 'https://github.com/cloudify-cosmo/cloudify-ansible-plugin/' \
           'releases/download/{v}/cloudify_ansible_plugin' \
           '-{v}-py27-none-linux_x86_64-centos-Core.wgn'.format(v=AN_VERSION)
AN_PLUGIN = 'https://github.com/cloudify-cosmo/cloudify-ansible-plugin/' \
            'releases/download/{v}/plugin.yaml'.format(v=AN_VERSION)

PLUGINS_TO_UPLOAD = [(OS_WAGON, OS_PLUGIN),
                     (TF_WAGON, TF_PLUGIN),
                     (UT_WAGON, UT_PLUGIN),
                     (AN_WAGON, AN_PLUGIN),
                     (DK_WAGON, DK_PLUGIN)]

SECRETS_TO_CREATE = {
    'aws_access_key_id': False,
    'aws_secret_access_key': False,
    'aws_region_name': False,
    'ec2_region_endpoint': False,
    'azure_subscription_id': False,
    'azure_tenant_id': False,
    'azure_client_id': False,
    'azure_client_secret': False,
    'azure_location': False,
    'openstack_username': False,
    'openstack_password': False,
    'openstack_tenant_name': False,
    'openstack_auth_url': False,
    'openstack_region': False,
    'openstack_region_name': False,
    'openstack_external_network': False,
    'openstack_project_id': False,
    'openstack_project_name': False,
    'openstack_project_domain_id': False,
    'openstack_user_domain_name': False,
    'openstack_project_domain_name': False,
    'base_image_id': False,
    'base_flavor_id': False,
    'gcp_credentials': True,
    'openshift_secret_token': False,
    'openshift_master_endpoint': False,
    'vsphere_username': False,
    'vsphere_password': False,
    'vsphere_host': False,
    'vsphere_port': False,
    'vsphere_datacenter_name': False,
    'vsphere_resource_pool_name': False,
    'vsphere_auto_placement': False,
    'vsphere_centos_template': False,
    'vsphere_private_key': True,
    'vsphere_public_key': True
}


def get_supported_examples():
    with open(SUPPORTED_EXAMPLES_FILE, 'r') as outfile:
        return load_json(outfile, object_pairs_hook=OrderedDict)


# This structure tells us which files to support.
SUPPORTED_EXAMPLES = get_supported_examples()

# Let's make a list of supported blueprint files.
blueprint_list = ['{0}/{1}/{2}'.format(CWD, dirname, filename)
                  for dirname, filelist in SUPPORTED_EXAMPLES.items()
                  for filename in filelist]


class VersionsException(Exception):
    pass


def get_cloudify_version():
    """Let's get the Cloudify versions of the blueprints.
    We need them to make sure they are all the same in the tests.
    And also to get the cloudify version for the release.
    """

    cloudify_version = None
    # Loop through each blueprint file.
    for blueprint_file in blueprint_list:
        # Load the blueprint YAML as a dictionary.
        with open(blueprint_file, 'r') as stream:
            try:
                blueprint_yaml = yaml_load(stream)
            except YAMLError as e:
                raise VersionsException(
                    'Problem with the file: {0}...{1}'.format(
                        blueprint_file, str(e)))

        # Loop through the imports
        for blueprint_import in blueprint_yaml['imports']:
            import_url = urlparse(blueprint_import)
            if import_url.netloc != 'cloudify.co':
                # It's not a cloudify.co import.
                continue
            next_version = import_url.path.split('/')[-2:-1]
            if isinstance(next_version, list):
                next_version = next_version.pop()
            if not isinstance(next_version, basestring):
                raise VersionsException(
                    'Cloudify version problem: {0}'.format(cloudify_version))
            if cloudify_version and next_version != cloudify_version:
                raise VersionsException(
                    'Cloudify version mismatch: {0}/{1} from {2}'.format(
                        cloudify_version, next_version, blueprint_file))
            cloudify_version = next_version
    return cloudify_version


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
