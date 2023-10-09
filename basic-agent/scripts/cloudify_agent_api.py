from time import sleep

from cloudify import ctx
from cloudify.state import ctx_parameters
from cloudify_agent.installer.operations import create


def create_ext(*args, **kwargs):
    cloudify_agent = ctx.instance.runtime_properties.get('cloudify_agent')
    if not cloudify_agent:
        ctx.logger.info('Running cloudify agent install...')
        create(*args, **kwargs)
    sleep(60)


if __name__ == '__main__':
    create_ext(**ctx_parameters)
