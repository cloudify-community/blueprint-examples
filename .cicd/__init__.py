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

from os import path
from yaml import load as yaml_load, YAMLError

CWD = '/{0}'.format(
    '/'.join(path.abspath(path.dirname(__file__)).split('/')[1:-1],))

# This structure tells us which files to support.
SUPPORTED_EXAMPLES = (
    ('aws-example-network',
        ['blueprint.yaml']),
    ('azure-example-network',
        ['blueprint.yaml']),
    ('gcp-example-network',
        ['blueprint.yaml']),
    ('openstack-example-network',
        ['blueprint.yaml']),
    ('hello-world-example',
        ['aws.yaml', 'azure.yaml', 'gcp.yaml', 'openstack.yaml']),
    ('open-source-vnf/connected_host',
        ['openstack.yaml']),
    ('open-source-vnf/network_topology',
        ['openstack.yaml']),
    ('open-source-vnf/httpd',
        ['openstack.yaml']),
    ('open-source-vnf/haproxy',
        ['openstack.yaml']),
    ('open-source-vnf/pfsense',
        ['openstack.yaml']),
    ('open-source-vnf/service',
        ['service-chaining.yaml']),
)

# Let's make a list of supported blueprint files.
blueprint_list = ['{0}/{1}/{2}'.format(CWD, dirname, filename)
                  for dirname, filelist in SUPPORTED_EXAMPLES
                  for filename in filelist]


class VersionsException(Exception):
    pass


def get_cloudify_version():
    """Let's get the Cloudify versions of the blueprints.
    We need them to make sure they are all the same in the tests.
    And also to get the cloudify version for the release.
    """

    cloudify_version = None
    for blueprint_file in blueprint_list:
        with open(blueprint_file, 'r') as stream:
            try:
                blueprint_yaml = yaml_load(stream)
                next_version = \
                    blueprint_yaml['imports'][0].split('/')[-2:-1][0]
                if cloudify_version and next_version != cloudify_version:
                    raise VersionsException(
                        'Cloudify version mismatch: {0}/{1} from {2}'.format(
                            cloudify_version, next_version, blueprint_file))
                cloudify_version = next_version
            except (YAMLError, IndexError, KeyError) as e:
                raise VersionsException(
                    'Problem with the file: {0}...{1}'.format(
                        blueprint_file, str(e)))
    return cloudify_version
