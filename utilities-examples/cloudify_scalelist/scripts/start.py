#!/usr/bin/env python
#
# Copyright (c) 2018 Cloudify Platform Ltd. All rights reserved
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

# How to test:
# Install the blueprint:
# cfy install examples/blueprint.yaml
# Execute scaleuplist twice:
# cfy executions start scaleuplist -p examples/scaleup_params.yaml
# Within 150 SSH into the manager and kill one of the script executions.


from time import sleep

from cloudify import ctx
from cloudify import manager

if __name__ == '__main__':
    client = manager.get_rest_client()
    result = client.node_instances.list(node_id=ctx.node.id)

    if len(result) >= 5:
        sleep(150)
