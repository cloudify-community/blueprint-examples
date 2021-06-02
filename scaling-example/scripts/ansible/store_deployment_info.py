import json
from os import path

from cloudify import ctx

INFO_FILE_PATH = path.join("/", "tmp", "virtual-machine-example-vars.json")

with open(INFO_FILE_PATH, "r") as vars_file:
    ctx.instance.runtime_properties.update(json.load(vars_file))
