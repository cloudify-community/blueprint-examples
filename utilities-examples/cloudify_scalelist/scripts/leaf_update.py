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
    # use properties provided by current node
    if 'config' not in ctx.instance.runtime_properties:
        ctx.instance.runtime_properties['config'] = {}
    properties.update(ctx.instance.runtime_properties['config'])
    # use properties provided by workflow parameters
    properties.update(inputs)
    ctx.logger.info("Resulted properties: {}".format(properties))

    runtime_properties = ctx.instance.runtime_properties['config']
    runtime_properties["width"] = properties["width"]
    ctx.instance.runtime_properties['config'] = runtime_properties
    ctx.logger.info("We will update: {}".format(
                    repr(ctx.instance.runtime_properties)))
