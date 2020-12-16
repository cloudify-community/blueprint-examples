from cloudify import ctx

if __name__ == '__main__':
    for output in ctx.instance.runtime_properties['Outputs']:
        if output['OutputKey'] == 'IP':
            ctx.instance.runtime_properties['ip'] = output['OutputValue']
