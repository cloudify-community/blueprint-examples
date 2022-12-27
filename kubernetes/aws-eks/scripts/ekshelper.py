
from cloudify import ctx
from cloudify.manager import get_rest_client
from cloudify.exceptions import OperationRetry


ISSUER_TEMPLATE = 'arn:aws:iam::{}:oidc-provider/' \
                  'oidc.eks.region-code.amazonaws.com/id/{}'


def update_cluster():
    client = get_rest_client()
    client.executions.start(
        ctx.deployment.id,
        workflow_id='execute_operation',
        force=True,
        parameters={
            'operation': 'cloudify.interfaces.lifecycle.poststart',
            'node_ids': ['eks_cluster'],
        }
    )


if __name__ == "__main__":
    resource_config = ctx.node.properties.get('resource_config', {})
    issuer = resource_config.get('issuer')
    region_name = resource_config.get('aws_region_name')
    account_id = resource_config.get('account_id')
    if not issuer:
        update_cluster()
        raise OperationRetry('Waiting for issuer data...')

    issuer_value = issuer.split('/')[-1]
    aud = 'oidc.eks.{}.amazonaws.com/id/{}:aud'.format(
        region_name, issuer_value)
    sub = 'oidc.eks.{}.amazonaws.com/id/{}:sub'.format(
        region_name, issuer_value)
    ctx.instance.runtime_properties['condition'] = {
        'StringEquals': {
            aud: 'sts.amazonaws.com',
            sub: 'system:serviceaccount:kube-system:ebs-csi-controller-sa'
        }
    }
    ctx.instance.runtime_properties['federated'] = ISSUER_TEMPLATE.format(
        account_id, issuer_value)
    ctx.instance.runtime_properties['role_name'] = \
        'AmazonEKS_EBS_CSI_DriverRole_' + issuer_value
