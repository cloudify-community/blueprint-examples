import os
import tempfile

from cloudify import ctx

f = tempfile.NamedTemporaryFile(delete=False,
                                suffix='__ansible_aws_infra_info__')
ctx.instance.runtime_properties['ansible_infra_info_file'] = os.path.abspath(
    f.name)
