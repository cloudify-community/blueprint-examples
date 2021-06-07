import json
from os import path

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

file_path = inputs.get('infra_info_file')
with open(file_path, "r") as vars_file:
    ctx.instance.runtime_properties.update(json.load(vars_file))
