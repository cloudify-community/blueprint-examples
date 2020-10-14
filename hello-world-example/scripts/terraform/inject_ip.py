import base64
from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

if __name__ == '__main__':
    terraform_node = ctx.instance.runtime_properties
    ctx.instance.runtime_properties['ip'] = inputs['ip']
