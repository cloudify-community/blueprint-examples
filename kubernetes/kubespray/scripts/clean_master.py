from fabric.api import run
from cloudify import ctx


def remove_node(*argc, **kargs):
    hostname = ctx.source.instance.id
    hostname = hostname.replace('_', '-')
    hostname = hostname.lower()
    ctx.logger.info('Remove node instance: {hostname}'
                    .format(hostname=hostname))
    run('kubectl delete node {hostname}'.format(hostname=hostname))
