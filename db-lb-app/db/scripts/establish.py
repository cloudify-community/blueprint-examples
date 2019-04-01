from cloudify import ctx

if __name__ == '__main__':

    ctx.logger.info('Gather cluster data.')

    mariadb_props = ctx.source.instance.runtime_properties
    cluster_props = ctx.target.instance.runtime_properties

    if 'cluster_members' not in cluster_props:
        cluster_props['cluster_members'] = []

    groups = mariadb_props.get(
        'sources', {}).get('all', {}).get('children', {})

    ctx.logger.info('Cluster groups: {0}'.format(groups))

    for group_name, group in groups.items():
        if group_name == 'galera_cluster':
            ctx.logger.info('Group hosts: {0}'.format(group['hosts']))
            for hostname, host in group['hosts'].items():
                cluster_props['cluster_members'].append(
                    {
                        'name': hostname,
                        'address': host['ansible_host']
                    }
                )

    ctx.logger.info('Finished gathering cluster data.')
