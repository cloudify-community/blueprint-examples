from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

# Storing the port of the input as the integer value for containerPort
CALC_PORT =  int(inputs['EXTERNAL_NODE_PORT_BASE']) + int(inputs['INSTANCE_INDEX'])
ctx.instance.runtime_properties['node_port'] = CALC_PORT
ctx.logger.info("stored runtime-prop NODE_PORT as {0} ".format(CALC_PORT))
