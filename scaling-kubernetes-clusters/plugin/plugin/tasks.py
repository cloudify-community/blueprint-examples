import pytz
import requests
import datetime
from cloudify import manager
from cloudify_rest_client import CloudifyClient
from cloudify_rest_client.executions import Execution
from cloudify import ctx


TIMESTAMP_FORMAT = '%Y%m%d%H%M'
LAST_SCLAING_TIMESTAMP_RP = 'last_scaling_timestamp'
LAST_SCLAING_EXECUTION_ID = 'last_scaling_execution_id'
SCALEOUTS_RP = 'scaleouts'

def _get_client(client_config=None):
    if client_config is not None:
        return CloudifyClient(**client_config)
    return manager.get_rest_client()


def _check(url, url_timeout, low_threshold, high_threshold):
    try:
        resp_time = requests.get(url,
            timeout=url_timeout).elapsed.total_seconds() * 1000

        ctx.logger.debug("{} replied in {} miliseconds".format(url, resp_time))

        if  resp_time <  low_threshold:
            return -1
        if resp_time >  high_threshold:
            return 1
    except requests.exceptions.Timeout:
        ctx.logger.debug("{} timed out".format(url))
    except requests.exceptions.RequestException:
        ctx.logger.debug("{} request failed".format(url))

    return 0

def _schedule(node_id,
              interval,
              client_config=None,
              operation='cloudify.interfaces.lifecycle.start'):
    client = _get_client(client_config)

    parameters = {
        'operation': operation,
        'allow_kwargs_override': False,
        'node_ids': [node_id],
        'node_instance_ids': [],
        'operation_kwargs': {},
        'run_by_dependency_order': False,
        'type_names': []
        }

    # schedule format must be YYYYMMDDHHMM+HHMM or YYYYMMDDHHMM-HHMM
    schedule_time = (datetime.datetime.now() + \
                    datetime.timedelta(minutes=interval)).replace(
                        tzinfo=pytz.utc).strftime(TIMESTAMP_FORMAT+'%z')

    client.executions.start(deployment_id=ctx.deployment.id,
                            workflow_id='execute_operation',
                            parameters=parameters,
                            schedule=schedule_time)

def _execute_scale(deployment_id,
                   scalable_entity_name,
                   delta,
                   client_config=None):
    client = _get_client(client_config)

    parameters = {
        'operation':
            'scale_nodes.scale_up' if delta>0 else 'scale_nodes.scale_down',
        'allow_kwargs_override': True,
        'node_ids': [scalable_entity_name],
        'node_instance_ids': [],
        'operation_kwargs': {
            'delta': delta,
        },
        'run_by_dependency_order': False,
        'type_names': []
        }

    return client.executions.start(
        deployment_id=deployment_id,
        workflow_id='execute_operation',
        parameters= parameters
    )

def check_if_scale_finished(execution_id, client_config=None):
    if execution_id is None:
        return True
    client = _get_client(client_config)
    included_fields = ['id', 'status']
    execution = client.executions.get(execution_id, _include=included_fields)
    if execution.status in Execution.END_STATES:
        return True
    return False


def _scale_up(deployment_id,
              scalable_entity_name,
              delta,
              client_config=None):
    execution_id = ctx.instance.runtime_properties.get(
        LAST_SCLAING_EXECUTION_ID,
        None)
    if check_if_scale_finished(execution_id, client_config):
        ctx.instance.runtime_properties[LAST_SCLAING_EXECUTION_ID] = \
            _execute_scale(deployment_id=deployment_id,
                scalable_entity_name=scalable_entity_name,
                delta=delta,
                client_config=client_config).id
        return True
    return False

def _scale_down(deployment_id,
                scalable_entity_name,
                delta,
                client_config=None):
    execution_id = ctx.instance.runtime_properties.get(
        LAST_SCLAING_EXECUTION_ID,
        None)
    if check_if_scale_finished(execution_id, client_config):
        ctx.instance.runtime_properties[LAST_SCLAING_EXECUTION_ID] = \
            _execute_scale(deployment_id=deployment_id,
                scalable_entity_name=scalable_entity_name,
                delta=-1 * delta,
                client_config=client_config).id
        return True
    return False

def _cooldown_exceeded(last_execution_str, cooldown):
    if last_execution_str is None:
        return True
    return datetime.datetime.now() - datetime.timedelta(minutes=cooldown) > \
        datetime.datetime.strptime(last_execution_str,
                                   TIMESTAMP_FORMAT)

def _get_args_or_property(name, args):
    return args.get(name, ctx.node.properties.get(name, None))

def check_and_schedule(**inputs):
    deployment_id = _get_args_or_property('deployment_id', inputs)
    scalable_entity_name = _get_args_or_property('scalable_entity_name', inputs)
    client = _get_args_or_property('client', inputs)
    delta = _get_args_or_property('delta', inputs)
    url = _get_args_or_property('url', inputs)
    low_threshold = _get_args_or_property('low_threshold', inputs)
    high_threshold = _get_args_or_property('high_threshold', inputs)
    scaleup_cooldown = _get_args_or_property('scaleup_cooldown', inputs)
    scaledown_cooldown = _get_args_or_property('scaledown_cooldown', inputs)
    interval = _get_args_or_property('interval', inputs)
    scaleout_limit = _get_args_or_property('scaleout_limit', inputs)

    last_execution_str = ctx.instance.runtime_properties.get(
        LAST_SCLAING_TIMESTAMP_RP,
        None)

    scaleouts = ctx.instance.runtime_properties.get(
        SCALEOUTS_RP,
        0)

    scale_executed = False
    url_timeout = interval * 60
    check_result = _check(url, url_timeout, low_threshold, high_threshold)
    if  check_result > 0 and \
        _cooldown_exceeded(last_execution_str, scaleup_cooldown) and \
        scaleouts < scaleout_limit:
        scale_executed = \
            _scale_up(deployment_id, scalable_entity_name, delta, client)
        if scale_executed:
            scaleouts += 1

    elif check_result < 0 and _cooldown_exceeded(last_execution_str,
        scaledown_cooldown) and scaleouts > 0:
        scale_executed = \
            _scale_down(deployment_id, scalable_entity_name, delta, client)
        if scale_executed:
            scaleouts -= 1

    _schedule(ctx.node.id, interval, client)

    if scale_executed:
        ctx.instance.runtime_properties[LAST_SCLAING_TIMESTAMP_RP] = \
             datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
        ctx.instance.runtime_properties[SCALEOUTS_RP] = scaleouts
