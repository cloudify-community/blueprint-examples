from cloudify.state import ctx_parameters as inputs
from cloudify.manager import get_rest_client


client = get_rest_client()
client.secrets.create('kubernetes_token',  inputs['kube_token'])
