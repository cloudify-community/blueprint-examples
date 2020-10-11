from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
if __name__ == '__main__':
    ctx.logger.info('Gather inventory data.')
    ansible_node = ctx.source.instance.runtime_properties
    terraform_node = ctx.target.instance.runtime_properties
    if 'sources' not in ansible_node:
        ansible_node['sources'] = {
            'cloud_resources': {
                'hosts': {
                }
            }
        }
    for cloud_resource_compute in terraform_node['resources']['eip']['instances']:
        ansible_inventory_entry = {
            cloud_resource_compute['attributes']['public_ip']: {
                'ansible_host': cloud_resource_compute['attributes']['public_ip'],
                'ansible_user': inputs.get('agent_user'),
                'ansible_become': True,
                'ansible_ssh_private_key_file': inputs.get('private_key'),
                'ansible_ssh_common_args': '-o StrictHostKeyChecking=no'
            }
        }
        ansible_node['sources']['cloud_resources']['hosts'].update(ansible_inventory_entry)
