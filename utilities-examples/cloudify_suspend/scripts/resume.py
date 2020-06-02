from cloudify import ctx

resource_id = ctx.node.properties.get('resource_id')
ctx.logger.info('resume server_id={}'.format(resource_id))
