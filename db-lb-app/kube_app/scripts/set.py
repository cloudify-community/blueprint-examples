from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

# Storing the port of the input as the integer value for containerPort
ctx.instance.runtime_properties['ports.containerPort'] = int(inputs['PORT'])
ctx.logger.info("stored runtime-prop containerPort as {0} ".format(inputs['PORT']))
