import base64

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
from cloudify.manager import get_rest_client


client = get_rest_client()
token = base64.b64decode(inputs['kube_token']).decode('utf-8')
client.secrets.create('kubernetes_token',  token, update_if_exists=True)
ctx.instance.runtime_properties['token'] = token
