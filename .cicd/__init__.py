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

SUPPORTED_EXAMPLES = (
    ('aws-example-network', ['blueprint.yaml']),
    ('azure-example-network', ['blueprint.yaml']),
    ('gcp-example-network', ['blueprint.yaml']),
    ('openstack-example-network', ['blueprint.yaml']),
    ('hello-world-example',
        ['aws.yaml', 'azure.yaml', 'gcp.yaml', 'openstack.yaml'])
)
