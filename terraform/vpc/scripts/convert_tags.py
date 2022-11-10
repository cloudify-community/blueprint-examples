#!/usr/bin/env python

from cloudify import ctx
from cloudify.state import ctx_parameters

for key in ['vpc_tags', 'subnet_1_tags', 'subnet_2_tags']:
    print(key)
    print(ctx_parameters[key])
    ctx.instance.runtime_properties[key] = { item['Key']: item['Value'] for item in ctx_parameters[key]}
