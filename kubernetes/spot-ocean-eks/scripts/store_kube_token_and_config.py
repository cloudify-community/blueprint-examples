import base64
import json

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
from cloudify.manager import get_rest_client

client = get_rest_client()
token = base64.b64decode(inputs['kube_token']).decode('utf-8')
client.secrets.create('kubernetes_token', token, update_if_exists=True)
ctx.instance.runtime_properties['token'] = token
kube_config = json.dumps(inputs['kube_config'])
client.secrets.create('kubernetes_config', kube_config, update_if_exists=True)
ctx.instance.runtime_properties['kube_config'] = kube_config
