from fabric2 import task

from cloudify import ctx


@task
def remove_node(connection, *argc, **kargs):
    hostname = ctx.source.instance.id
    hostname = hostname.replace('_', '-')
    hostname = hostname.lower()
    ctx.logger.info('Remove node instance: {hostname}'
                    .format(hostname=hostname))
    connection.run('kubectl delete node {hostname}'.format(hostname=hostname))
