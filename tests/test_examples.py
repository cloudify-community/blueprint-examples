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

from os import path, system
from unittest import TestCase


class TestExamples(TestCase):
    """These tests cover blueprint validation."""

    @property
    def cwd(self):
        return '/{0}'.format(
            '/'.join(
                path.abspath(
                    path.dirname(__file__)
                ).split('/')[1:-1],
            )
        )

    @staticmethod
    def upload_blueprint(blueprint_path):
        """Successfully uploading a
        blueprint indicates that it is valid according to the DSL.
        """
        print blueprint_path
        result = system('cfy blueprints upload {0}'.format(blueprint_path))
        return True if result is 0 else False

    def test_aws_example_network(self):
        blueprint_path = path.join(
            self.cwd, 'aws-example-network', 'blueprint.yaml')
        self.assertTrue(self.upload_blueprint(blueprint_path))

    def test_azure_example_network(self):
        blueprint_path = path.join(
            self.cwd, 'azure-example-network', 'blueprint.yaml')
        self.assertTrue(self.upload_blueprint(blueprint_path))

    def test_gcp_example_network(self):
        blueprint_path = path.join(
            self.cwd, 'gcp-example-network', 'blueprint.yaml')
        self.assertTrue(self.upload_blueprint(blueprint_path))

    def test_openstack_example_network(self):
        blueprint_path = path.join(
            self.cwd, 'openstack-example-network', 'blueprint.yaml')
        self.assertTrue(self.upload_blueprint(blueprint_path))

    def test_hello_world_example(self):
        for blueprint_file_name in \
                ['aws.yaml', 'azure.yaml', 'gcp.yaml', 'openstack.yaml']:
            blueprint_path = path.join(
                self.cwd, 'hello-world-example', blueprint_file_name)
            self.assertTrue(self.upload_blueprint(blueprint_path))
