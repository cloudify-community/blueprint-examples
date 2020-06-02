from cloudify import ctx
from cloudify import exceptions as cfy_exc
from cloudify.state import ctx_parameters as inputs


if __name__ == '__main__':

    raise_failure = inputs.get('failure')
    if raise_failure == ctx.operation.name:
        raise cfy_exc.NonRecoverableError('Hey check, i am failure')
