#!/opt/manager/env/bin/python
import sys
from copy import deepcopy

from manager_rest.flask_utils import setup_flask_app
from manager_rest.storage import get_storage_manager, models
from manager_rest.manager_exceptions import NotFoundError
from manager_rest.resource_manager import ResourceManager


def cleanup_deployment(depl_id, get_all):
    with setup_flask_app().app_context():
        sm = get_storage_manager()
        params_filter = ResourceManager.create_filters_dict(
            deployment_id=depl_id)
        list_kwargs = {
            'filters': params_filter,
            'include': None
        }
        if get_all:
            list_kwargs['get_all_results'] = True

        instances = get_storage_manager().list(
            models.NodeInstance, **list_kwargs
        ).items
        alive_instances = []
        delete_instances = []
        count_instances = {}
        for instance in instances:
            if instance.node_id not in count_instances:
                count_instances[instance.node_id] = 0
            if instance.state not in ('uninitialized', 'deleted'):
                alive_instances.append(instance.id)
                # update count of instances internaly
                count_instances[instance.node_id] += 1
            else:
                delete_instances.append(instance.id)
                sm.delete(instance)
        sys.stderr.write("For save as alive: {}\n"
                         .format(repr(alive_instances)))
        sys.stderr.write("For delete as uninitialized: {}\n"
                         .format(repr(delete_instances)))
        # cleanup instances relationships
        for instance in instances:
            if instance.id in alive_instances:
                sys.stderr.write("{}:Before relationships{}\n".format(
                    instance.id, repr(instance.relationships)))
                relationships = []
                for relationship in instance.relationships:
                    if relationship['target_id'] in alive_instances:
                        relationships.append(relationship)
                instance.relationships = relationships
                sys.stderr.write("{}:After relationships{}\n".format(
                    instance.id, repr(instance.relationships)))
                sm.update(instance)
        # cleanup nodes
        nodes = get_storage_manager().list(models.Node, **list_kwargs).items
        for node in nodes:
            if node.id in count_instances:
                node.number_of_instances = count_instances[node.id]
                sm.update(node)
        sys.stderr.write("Count instances after cleanup: {}\n"
                         .format(repr(count_instances)))
        # deployemnts update
        deployment = sm.get(
            models.Deployment,
            depl_id
        )
        sys.stderr.write("Scaling groups before: {}\n"
                         .format(repr(deployment.scaling_groups)))
        scaling_groups = deepcopy(deployment.scaling_groups)
        for scaling_group_name in scaling_groups:
            scaling_group = scaling_groups[scaling_group_name]
            instances_count = 0
            for node in scaling_group['members']:
                if instances_count < count_instances.get(node, 0):
                    instances_count = count_instances[node]
            scaling_group['properties']['planned_instances'] = instances_count
            scaling_group['properties']['current_instances'] = instances_count
        deployment.scaling_groups = scaling_groups
        sm.update(deployment)
        sys.stderr.write("Scaling groups after: {}\n"
                         .format(repr(scaling_groups)))


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        sys.stderr.write(
            'Usage: {prog} <deployment id> {{page, all}}\n'.format(
                prog=sys.argv[0],
            )
        )
        sys.exit(1)
    depl_id = sys.argv[1]
    get_all = False
    if len(sys.argv) == 3 and sys.argv[2] == 'all':
        get_all = True

    try:
        cleanup_deployment(depl_id, get_all)
    except NotFoundError:
        sys.stderr.write(
            'Could not find deployment: {depl_id}\n'.format(
                depl_id=depl_id,
            )
        )
        sys.exit(2)
    except Exception as ex:
        sys.stderr.write(
            'Aborting! '
            "Can't cleanup deployment: {depl_id}\nError: {error}".format(
                depl_id=depl_id, error=repr(ex)
            )
        )
        sys.exit(3)
    print('Successfully cleaned up deployment: {depl_id}'.format(
        depl_id=depl_id,
    ))
