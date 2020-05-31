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

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs


if __name__ == '__main__':
    ctx.logger.info("I am {}".format(repr(ctx.instance.id)))

    properties = {}
    # use properties provided by install
    properties.update(ctx.node.properties)
    # use properties provided by runtime_propoerties from other instances
    properties.update(inputs)
    # use properties provided by current node
    if 'config' not in ctx.instance.runtime_properties:
        ctx.instance.runtime_properties['config'] = {}
    properties.update(ctx.instance.runtime_properties['config'])
    ctx.logger.info("Resulted properties: {}".format(properties))

    if properties.get("resource_id"):
        ctx.logger.error("We already have resource {}? "
                         .format(repr(properties["resource_id"])))
    else:
        runtime_properties = ctx.instance.runtime_properties['config']
        runtime_properties["resource_id"] = ctx.instance.id
        runtime_properties["name"] = properties.get("name")
        runtime_properties["branch_name"] = properties["branch_name"]
        runtime_properties["leaf_name"] = properties["leaf_name"]
        # convert scale inputs to correct names
        convert_table = ctx.node.properties.get('convert_inputs', {})
        for input_name in convert_table:
            if input_name in properties:
                runtime_properties[
                    convert_table[input_name]] = properties[input_name]
        ctx.instance.runtime_properties['config'] = runtime_properties
        # Write that we created everyting
        ctx.logger.info("We will create: {}".format(
            repr(ctx.instance.runtime_properties)))
