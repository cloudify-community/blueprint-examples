import os
from cloudify import ctx

tempfile = ctx.instance.runtime_properties.get('ansible_infra_info_file')
if os.path.isfile(tempfile):
    os.remove(tempfile)
    ctx.logger.info("Deleted file: {path}".format(path=tempfile))
else:
    ctx.logger.info("file: {path} does not exist.".format(path=tempfile))
