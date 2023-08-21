import io
import os
import tempfile

from cloudify import ctx
from cloudify.exceptions import NonRecoverableError

try:
    import docker
except ImportError:
    raise NonRecoverableError('no docker!')


def get_config_from_props(prop_name, default=None):
    default = default or {}
    return ctx.node.properties.get(prop_name, {})


def get_client_config():
    return get_config_from_props('client_config')


def get_resource_config():
    return get_config_from_props('resource_config')


def is_operation(desired):
    operation_name = ctx.operation.name.split(
        'cloudify.interfaces.lifecycle.')[-1]
    return desired == operation_name


def is_precreate():
    return is_operation('precreate')


def is_create():
    return is_operation('create')


def is_stop():
    return is_operation('stop')


def is_delete():
    return is_operation('delete')


def build_image():
    cloudify_agent = ctx.instance.runtime_properties.get('cloudify_agent', {})
    endpoint = cloudify_agent.get('rest_host', ctx.rest_host)
    if not isinstance(endpoint, str):
        endpoint = endpoint[0]
    dirpath = tempfile.mkdtemp()
    ctx.download_resource_and_render(
        'resources/Dockerfile',
        os.path.join(dirpath, 'Dockerfile'),
        {
            'TOKEN': ctx.rest_token,
            'CM_ENDPOINT': endpoint,
            'TENANT_NAME': ctx.tenant_name,
            'DEPLOYMENT_ID': ctx.deployment.id,
            'COMPUTE_NODE_INSTANCE_ID': ctx.instance.id,
        })
    ctx.download_resource(
        'resources/_copyme.sh',
        os.path.join(dirpath, '_copyme.sh')
    )
    client_config = get_client_config()
    client = docker.DockerClient(**client_config)
    ctx.logger.info('Building image.')
    client.images.build(
        path=dirpath,
        tag='{}/latest'.format(ctx.instance.id),
        rm=True,
        forcerm=True)


def run_container():
    ctx.logger.info('Running docker container.')
    client_config = get_client_config()
    resource_config = get_resource_config()
    if 'image' not in resource_config:
        resource_config['image'] = '{}/latest'.format(ctx.instance.id)
    client = docker.DockerClient(**client_config)
    client.containers.run(**resource_config)


def stop_container():
    ctx.logger.info('Stopping docker container.')
    # client_config = get_client_config()
    # resource_config = get_resource_config()
    # if 'image' not in resource_config:
    #     resource_config['image'] = '{}/latest'.format(ctx.instance.id)
    # client = docker.DockerClient(**client_config)
    # container = client.containers.get(resource_config['name'])
    # container.stop()


def delete_image():
    ctx.logger.info('Deleting image.')
    # client_config = get_client_config()
    # client = docker.DockerClient(**client_config)
    # container = client.images.get('{}/latest'.format(ctx.instance.id))


if __name__ == '__main__':

    if is_precreate():
        build_image()
    elif is_create():
        run_container()
    elif is_stop():
        stop_container()
    elif is_delete():
        delete_image()
    else:
        ctx.logger.error('Unsupported operation: {}'.format(ctx.operation.name))
        raise Exception('Retrying....')
