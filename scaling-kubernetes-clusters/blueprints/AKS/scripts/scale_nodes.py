import sys
PY2 = sys.version_info[0] == 2

import copy
import time
import json
import requests

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

if PY2:
    import httplib
else:
    import http.client as httplib

def authorize_with_azure():

    azure_tenant = inputs['azure_config']['tenant_id']
    azure_client_id = inputs['azure_config']['client_id']
    azure_secret = inputs['azure_config']['client_secret']

    url = "https://login.microsoftonline.com/{0}/oauth2/token".format(
        azure_tenant)
    body = {
        "resource" : "https://management.core.windows.net/",
        "client_id" : azure_client_id,
        "grant_type" : "client_credentials",
        "client_secret" : azure_secret
    }
    response = requests.post(url, data=body)
    return response.json()


def get_agent_pool():
    azure_subscription_id = inputs['azure_config']['subscription_id']
    resource_group_name = inputs['resource_group_name']
    cluster_name = inputs['cluster_name']
    agent_pool_name = inputs['agent_pool_name']
    url = "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerService/managedClusters/{resourceName}/agentPools/{agentPoolName}?api-version=2021-03-01".format(
            subscriptionId = azure_subscription_id,
            resourceGroupName = resource_group_name,
            resourceName = cluster_name,
            agentPoolName = agent_pool_name
        )
    headers = {
        'Authorization': 'Bearer ' + authorize_with_azure()['access_token'],
        'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)
    ctx.instance.runtime_properties['agent_pool'] = response.json()
    ctx.instance.runtime_properties['node_count'] = \
        response.json()['properties']['count']
    return response.json()


def scale_nodes():
    get_agent_pool()
    final_count = ctx.instance.runtime_properties['node_count'] + inputs['delta']
    azure_subscription_id = inputs['azure_config']['subscription_id']
    resource_group_name = inputs['resource_group_name']
    cluster_name = inputs['cluster_name']
    agent_pool_name = inputs['agent_pool_name']

    url = "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerService/managedClusters/{resourceName}/agentPools/{agentPoolName}?api-version=2021-03-01".format(
            subscriptionId = azure_subscription_id,
            resourceGroupName = resource_group_name,
            resourceName = cluster_name,
            agentPoolName = agent_pool_name
          )
    headers = {
        'Authorization': 'Bearer ' + authorize_with_azure()['access_token'],
        'Content-Type': 'application/json'
        }
    body = copy.deepcopy(ctx.instance.runtime_properties['agent_pool'])
    body['properties']['count'] = final_count
    response = requests.put(url, data=json.dumps(body), headers=headers)
    if response.status_code == httplib.OK:
        pool = response.json()
        while pool['properties']['provisioningState'] == 'Scaling':
            time.sleep(20)
            pool = get_agent_pool()
        ctx.instance.runtime_properties['agent_pool'] = pool
        ctx.instance.runtime_properties['node_count'] = \
            pool['properties']['count']
    else:
        raise Exception("Scale Failed {0}".format(response.json()))

if __name__ == '__main__':
    scale_nodes()
