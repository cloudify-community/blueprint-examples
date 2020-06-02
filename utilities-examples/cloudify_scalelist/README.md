# Cloudify Utilities: Scale List Workflow

## Description
Add support for scale several scalling group in one transaction.

For more information about this plugin, Read the full [documentation](https://github.com/cloudify-incubator/cloudify-utilities-plugin/tree/master/cloudify_scalelist).

## Examples

[Example](./blueprint.yaml) for show scaling several scaling group
within one transaction.

## Install with one "two" node

We install blueprint with one ["two" nodes](./blueprint.yaml).
```shell
$ cfy install cloudify-utilities-plugin/cloudify_scalelist/examples/blueprint.yaml -b examples
Uploading blueprint cloudify-utilities-plugin/cloudify_scalelist/examples/blueprint.yaml...
 blueprint.yaml |######################################################| 100.0%
Blueprint uploaded. The blueprint's id is examples
Creating new deployment from blueprint examples...
Deployment created. The deployment's id is examples
Executing workflow install on deployment examples [timeout=900 seconds]
Deployment environment creation is pending...
2018-06-28 08:53:39.574  CFY <examples> Starting 'create_deployment_environment' workflow execution
....
2018-06-28 08:54:00.628  CFY <examples> [one_l1grdr] Starting node
2018-06-28 08:54:01.631  CFY <examples> [two_o9pie8] Creating node
2018-06-28 08:54:01.631  CFY <examples> [two_o9pie8.create] Sending task 'script_runner.tasks.run'
2018-06-28 08:54:01.631  CFY <examples> [two_o9pie8.create] Task started 'script_runner.tasks.run'
2018-06-28 08:54:02.102  LOG <examples> [two_o9pie8.create] INFO: Downloaded scripts/create.py to /tmp/6P025/tmp3Vdq18-create.py
2018-06-28 08:54:03.020  LOG <examples> [two_o9pie8.create] INFO: Resulted properties: {u'predefined': u'', 'ctx': <cloudify.context.CloudifyContext object at 0x299e390>, u'script_path': u'scripts/create.py', u'resource_name': u'two0', u'defined_in_inputs': u'one_l1grdr'}
2018-06-28 08:54:03.020  LOG <examples> [two_o9pie8.create] INFO: We will create: two_o9pie8
2018-06-28 08:54:02.634  CFY <examples> [two_o9pie8.create] Task succeeded 'script_runner.tasks.run'
2018-06-28 08:54:03.637  CFY <examples> [two_o9pie8] Configuring node
2018-06-28 08:54:03.637  CFY <examples> [two_o9pie8] Starting node
2018-06-28 08:54:04.640  CFY <examples> [three_9qa5bk] Creating node
....
2018-06-28 08:54:14.666  CFY <examples> 'install' workflow execution succeeded
Finished executing workflow install on deployment examples
* Run 'cfy events list -e e2a944f6-f9cd-47f9-bd5c-5b5abf659d28' to retrieve the execution's events/logs
```

Check properties:
```shell
$ cfy node-instances get two_o9pie8
Retrieving node instance two_o9pie8

Node-instance:
+------------+---------------+---------+---------+---------+------------+----------------+------------+
|     id     | deployment_id | host_id | node_id |  state  | visibility |  tenant_name   | created_by |
+------------+---------------+---------+---------+---------+------------+----------------+------------+
| two_o9pie8 |  examples     |         |   two   | started |   tenant   | default_tenant |   admin    |
+------------+---------------+---------+---------+---------+------------+----------------+------------+

Instance runtime properties:
    resource_name: two0
    resource_id: two_o9pie8
```

## Install two additional 'two' nodes

Run scale [list up](examples/scaleup_params.yaml)
```shell
$ cfy executions start scaleuplist -d examples -p cloudify-utilities-plugin/cloudify_scalelist/examples/scaleup_params.yaml
Executing workflow scaleuplist on deployment examples [timeout=900 seconds]
2018-06-28 08:57:18.665  CFY <examples> Starting 'scaleuplist' workflow execution
2018-06-28 08:57:18.792  LOG <examples> INFO: Scale rules: {u'two_scale': {'count': 2, 'values': [{u'resource_name': u'two1'}, {u'resource_name': u'two2'}]}, u'four_scale': {'count': 3, 'values': [{u'resource_name': u'four1'}, {u'resource_name': u'four2'}, {u'resource_name': u'four3'}, {}, {}, {}]}}
2018-06-28 08:57:19.117  LOG <examples> INFO: Scale up u'two_scale' by delta: 2
2018-06-28 08:57:19.117  LOG <examples> INFO: Scale up u'four_scale' by delta: 3
2018-06-28 08:57:19.117  LOG <examples> INFO: Scale settings: {u'two_scale': {'instances': 3}, u'four_scale': {'instances': 4}}
2018-06-28 08:57:20.125  LOG <examples> INFO: Deployment modification started. [modification_id=f780db47-4e62-4e1a-8e1a-2fe2eafd768e]
2018-06-28 08:57:20.125  LOG <examples> INFO: Added: [u'three_dp5lqe', u'six_noqlic', u'three_nke3bw', u'four_3p58dr', u'six_ur7kbn', u'six_ajtm98', u'two_8b38ld', u'four_iqzzpd', u'two_czdur0', u'four_s4gpws', u'three_flgd5b']
2018-06-28 08:57:20.125  LOG <examples> INFO: Update node: two_czdur0
...
2018-06-28 08:57:21.752  CFY <examples> [two_czdur0] Creating node
2018-06-28 08:57:21.752  CFY <examples> [two_8b38ld.create] Task started 'script_runner.tasks.run'
2018-06-28 08:57:21.752  CFY <examples> [two_czdur0.create] Sending task 'script_runner.tasks.run'
2018-06-28 08:57:21.752  CFY <examples> [two_czdur0.create] Task started 'script_runner.tasks.run'
2018-06-28 08:57:22.153  LOG <examples> [two_8b38ld.create] INFO: Downloaded scripts/create.py to /tmp/WUJ2P/tmpMBIkmb-create.py
2018-06-28 08:57:23.142  LOG <examples> [two_8b38ld.create] INFO: Resulted properties: {u'predefined': u'', u'resource_name': u'two1', u'defined_in_inputs': u'one_l1grdr', u'_transaction_id': u'f780db47-4e62-4e1a-8e1a-2fe2eafd768e', u'script_path': u'scripts/create.py', 'ctx': <cloudify.context.CloudifyContext object at 0x287e390>}
2018-06-28 08:57:23.142  LOG <examples> [two_8b38ld.create] INFO: We will create: two_8b38ld
2018-06-28 08:57:23.142  LOG <examples> [two_czdur0.create] INFO: Downloaded scripts/create.py to /tmp/KQB80/tmpOxzvb_-create.py
2018-06-28 08:57:22.800  CFY <examples> [two_8b38ld.create] Task succeeded 'script_runner.tasks.run'
2018-06-28 08:57:23.142  LOG <examples> [two_czdur0.create] INFO: Resulted properties: {u'predefined': u'', u'resource_name': u'two2', u'defined_in_inputs': u'one_l1grdr', u'_transaction_id': u'f780db47-4e62-4e1a-8e1a-2fe2eafd768e', u'script_path': u'scripts/create.py', 'ctx': <cloudify.context.CloudifyContext object at 0x2e2b390>}
2018-06-28 08:57:23.142  LOG <examples> [two_czdur0.create] INFO: We will create: two_czdur0
2018-06-28 08:57:22.800  CFY <examples> [two_czdur0.create] Task succeeded 'script_runner.tasks.run'
...
2018-06-28 08:57:37.073  CFY <examples> [six_ur7kbn] Starting node
2018-06-28 08:57:38.076  CFY <examples> 'scaleuplist' workflow execution succeeded
Finished executing workflow scaleuplist on deployment examples
* Run 'cfy events list -e 9264cf6d-8e35-4004-a6f2-d4664193d309' to retrieve the execution's events/logs
```

Check properties:
```shell
$ cfy node-instances get two_czdur0
Retrieving node instance two_czdur0

Node-instance:
+------------+---------------+---------+---------+---------+------------+----------------+------------+
|     id     | deployment_id | host_id | node_id |  state  | visibility |  tenant_name   | created_by |
+------------+---------------+---------+---------+---------+------------+----------------+------------+
| two_czdur0 |  examples     |         |   two   | started |   tenant   | default_tenant |   admin    |
+------------+---------------+---------+---------+---------+------------+----------------+------------+

Instance runtime properties:
    resource_name: two2
    _transaction_id: f780db47-4e62-4e1a-8e1a-2fe2eafd768e
    resource_id: two_czdur0
```

## Remove instances created with resource_name=two2

Run scale [list down](examples/scaledown_params.yaml)
```shell
$ cfy executions start scaledownlist -d examples -p cloudify-utilities-plugin/cloudify_scalelist/examples/scaledown_params.yaml
Executing workflow scaledownlist on deployment examples [timeout=900 seconds]
2018-06-28 09:01:50.215  CFY <examples> Starting 'scaledownlist' workflow execution
2018-06-28 09:01:50.325  LOG <examples> INFO: List instances: {u'four': [u'four_iqzzpd', u'four_s4gpws', u'four_3p58dr'], u'six': [u'six_ajtm98', u'six_ur7kbn', u'six_noqlic'], u'two': [u'two_czdur0', u'two_8b38ld'], u'three': [u'three_dp5lqe', u'three_flgd5b', u'three_nke3bw']}
2018-06-28 09:01:51.329  LOG <examples> INFO: Scale rules: {u'two_scale': {'count': 2, 'values': [u'two_czdur0', u'two_8b38ld']}, u'four_scale': {'count': 3, 'values': [u'four_iqzzpd', u'four_s4gpws', u'four_3p58dr', u'six_ajtm98', u'six_ur7kbn', u'six_noqlic', u'three_dp5lqe', u'three_flgd5b', u'three_nke3bw']}}
2018-06-28 09:01:51.329  LOG <examples> INFO: Scale down u'two_scale' by delta: 2
2018-06-28 09:01:51.329  LOG <examples> INFO: Scale down u'four_scale' by delta: 3
2018-06-28 09:01:51.329  LOG <examples> INFO: Scale settings: {u'two_scale': {'instances': 1, 'removed_ids_include_hint': [u'two_8b38ld', u'two_czdur0']}, u'four_scale': {'instances': 1, 'removed_ids_include_hint': [u'four_3p58dr', u'four_iqzzpd', u'four_s4gpws', u'six_ajtm98', u'six_noqlic', u'six_ur7kbn', u'three_dp5lqe', u'three_flgd5b', u'three_nke3bw']}}
2018-06-28 09:01:51.329  LOG <examples> INFO: Deployment modification started. [modification_id=652e1a2a-7257-46f5-835b-96b3ccb6bfd5]
2018-06-28 09:01:51.329  LOG <examples> INFO: Removed: [u'three_9qa5bk', u'three_dp5lqe', u'six_noqlic', u'six_lr0xnq', u'two_o9pie8', u'three_nke3bw', u'four_3p58dr', u'six_ajtm98', u'two_czdur0', u'four_s4gpws', u'four_3hn6yy']
2018-06-28 09:01:51.329  LOG <examples> INFO: Proposed: [u'six_ajtm98', u'six_ur7kbn', u'six_noqlic', u'two_czdur0', u'two_8b38ld', u'three_dp5lqe', u'three_flgd5b', u'three_nke3bw', u'four_iqzzpd', u'four_s4gpws', u'four_3p58dr']
2018-06-28 09:01:51.329  LOG <examples> WARNING: Rolling back deployment modification. [modification_id=652e1a2a-7257-46f5-835b-96b3ccb6bfd5]: Exception("Instance u'two_o9pie8' not in proposed list [u'six_ajtm98', u'six_ur7kbn', u'six_noqlic', u'two_czdur0', u'two_8b38ld', u'three_dp5lqe', u'three_flgd5b', u'three_nke3bw', u'four_iqzzpd', u'four_s4gpws', u'four_3p58dr'].",)
2018-06-28 09:01:51.329  LOG <examples> INFO: Scale down based on transaction failed: Exception("Instance u'two_o9pie8' not in proposed list [u'six_ajtm98', u'six_ur7kbn', u'six_noqlic', u'two_czdur0', u'two_8b38ld', u'three_dp5lqe', u'three_flgd5b', u'three_nke3bw', u'four_iqzzpd', u'four_s4gpws', u'four_3p58dr'].",)
2018-06-28 09:01:52.169  CFY <examples> [six_noqlic] Stopping node
...
2018-06-28 09:02:02.551  CFY <examples> [two_czdur0] Deleting node
2018-06-28 09:02:02.551  CFY <examples> [two_8b38ld.delete] Sending task 'script_runner.tasks.run'
2018-06-28 09:02:02.551  CFY <examples> [two_8b38ld.delete] Task started 'script_runner.tasks.run'
2018-06-28 09:02:02.551  CFY <examples> [two_czdur0.delete] Sending task 'script_runner.tasks.run'
2018-06-28 09:02:02.551  CFY <examples> [two_czdur0.delete] Task started 'script_runner.tasks.run'
2018-06-28 09:02:02.881  LOG <examples> [two_8b38ld.delete] INFO: Downloaded scripts/delete.py to /tmp/GTDH5/tmp3xUMS9-delete.py
2018-06-28 09:02:03.381  LOG <examples> [two_8b38ld.delete] INFO: We have some resource u'two_8b38ld', so we can delete such
2018-06-28 09:02:03.381  LOG <examples> [two_8b38ld.delete] INFO: Resulted properties: {u'predefined': u'', u'resource_name': u'two1', u'defined_in_inputs': u'one_l1grdr', u'resource_id': u'two_8b38ld', 'ctx': <cloudify.context.CloudifyContext object at 0x24a2390>, u'_transaction_id': u'f780db47-4e62-4e1a-8e1a-2fe2eafd768e', u'script_path': u'scripts/delete.py'}
2018-06-28 09:02:03.381  LOG <examples> [two_czdur0.delete] INFO: Downloaded scripts/delete.py to /tmp/BMGFZ/tmpnnINzq-delete.py
2018-06-28 09:02:03.553  CFY <examples> [two_8b38ld.delete] Task succeeded 'script_runner.tasks.run'
2018-06-28 09:02:03.381  LOG <examples> [two_czdur0.delete] INFO: We have some resource u'two_czdur0', so we can delete such
2018-06-28 09:02:03.381  LOG <examples> [two_czdur0.delete] INFO: Resulted properties: {u'predefined': u'', u'resource_name': u'two2', u'defined_in_inputs': u'one_l1grdr', u'resource_id': u'two_czdur0', 'ctx': <cloudify.context.CloudifyContext object at 0x3b0b390>, u'_transaction_id': u'f780db47-4e62-4e1a-8e1a-2fe2eafd768e', u'script_path': u'scripts/delete.py'}
2018-06-28 09:02:03.553  CFY <examples> [two_czdur0.delete] Task succeeded 'script_runner.tasks.run'
2018-06-28 09:02:04.386  LOG <examples> INFO: Cleanup node: six_ajtm98
```

State after clean up:
```shell
$ cfy node-instances get two_czdur0
Retrieving node instance two_czdur0

Node-instance:
+------------+---------------+---------+---------+---------------+------------+----------------+------------+
|     id     | deployment_id | host_id | node_id |     state     | visibility |  tenant_name   | created_by |
+------------+---------------+---------+---------+---------------+------------+----------------+------------+
| two_czdur0 |  examples     |         |   two   | uninitialized |   tenant   | default_tenant |   admin    |
+------------+---------------+---------+---------+---------------+------------+----------------+------------+

Instance runtime properties:
```

## Uninstall

Run uninstall instances:
```shell
$ cfy uninstall examples
Executing workflow uninstall on deployment examples [timeout=900 seconds]
2018-06-28 09:04:03.146  CFY <examples> Starting 'uninstall' workflow execution
2018-06-28 09:04:04.414  CFY <examples> [six_lr0xnq] Stopping node
...
2018-06-28 09:04:16.482  CFY <examples> [one_l1grdr] Stopping node
2018-06-28 09:04:16.607  LOG <examples> [two_o9pie8.delete] INFO: We have some resource u'two_o9pie8', so we can delete such
2018-06-28 09:04:16.607  LOG <examples> [two_czdur0.delete] INFO: Downloaded scripts/delete.py to /tmp/TKV05/tmpw8btoN-delete.py
2018-06-28 09:04:16.482  CFY <examples> [two_8b38ld.delete] Task succeeded 'script_runner.tasks.run'
2018-06-28 09:04:16.482  CFY <examples> [two_o9pie8.delete] Task succeeded 'script_runner.tasks.run'
2018-06-28 09:04:16.607  LOG <examples> [two_czdur0.delete] INFO: Resulted properties: {u'predefined': u'', 'ctx': <cloudify.context.CloudifyContext object at 0x271b390>, u'script_path': u'scripts/delete.py', u'resource_name': u'two0', u'defined_in_inputs': u'one_l1grdr'}
2018-06-28 09:04:16.607  LOG <examples> [two_czdur0.delete] INFO: Not fully created instances, skip it
2018-06-28 09:04:16.482  CFY <examples> [two_czdur0.delete] Task succeeded 'script_runner.tasks.run'
2018-06-28 09:04:16.482  CFY <examples> [one_l1grdr] Stopping node
...
2018-06-28 09:04:18.611  LOG <examples> [one_l1grdr.delete] INFO: We have some resource u'one_l1grdr', so we can delete such
2018-06-28 09:04:18.489  CFY <examples> [one_l1grdr.delete] Task succeeded 'script_runner.tasks.run'
2018-06-28 09:04:19.491  CFY <examples> 'uninstall' workflow execution succeeded
Finished executing workflow uninstall on deployment examples
```

## Remove instances created by install workflow

State before [scale down](examples/scaledown_precreated.yaml):
```shell
$ cfy node-instances get two_05vh0m
Retrieving node instance two_05vh0m

Node-instance:
+------------+---------------+---------+---------+---------+------------+----------------+------------+
|     id     | deployment_id | host_id | node_id |  state  | visibility |  tenant_name   | created_by |
+------------+---------------+---------+---------+---------+------------+----------------+------------+
| two_05vh0m |    examples   |         |   two   | started |   tenant   | default_tenant |   admin    |
+------------+---------------+---------+---------+---------+------------+----------------+------------+

Instance runtime properties:
    resource_name: two0
    _transaction_id: two_precreated
    resource_id: two_05vh0m
```

Run scale down with instances with resource_name=two0 and same `transaction_id`.
```shell
$ cfy executions start scaledownlist -d examples -p cloudify-utilities-plugin/cloudify_scalelist/examples/scaledown_precreated.yaml
Executing workflow scaledownlist on deployment examples [timeout=900 seconds]
2018-07-02 11:03:41.396  CFY <examples> Starting 'scaledownlist' workflow execution
...
2018-07-02 11:03:51.730  CFY <examples> [two_05vh0m] Stopping node
2018-07-02 11:03:52.739  CFY <examples> [two_05vh0m] Deleting node
2018-07-02 11:03:52.739  CFY <examples> [two_05vh0m.delete] Sending task 'script_runner.tasks.run'
2018-07-02 11:03:52.739  CFY <examples> [two_05vh0m.delete] Task started 'script_runner.tasks.run'
2018-07-02 11:03:53.089  LOG <examples> [two_05vh0m.delete] INFO: Downloaded scripts/delete.py to /tmp/8IETC/tmp_fD831-delete.py
2018-07-02 11:03:53.626  LOG <examples> [two_05vh0m.delete] INFO: Resulted properties: {u'predefined': u'', u'resource_name': u'two0', u'defined_in_inputs': u'one_asu6fe', u'resource_id': u'two_05vh0m', 'ctx': <cloudify.context.CloudifyContext object at 0x311e390>, u'_transaction_id': u'two_precreated', u'script_path': u'scripts/delete.py'}
2018-07-02 11:03:53.626  LOG <examples> [two_05vh0m.delete] INFO: We have some resource u'two_05vh0m', so we can delete such
2018-07-02 11:03:53.743  CFY <examples> [two_05vh0m.delete] Task succeeded 'script_runner.tasks.run'
2018-07-02 11:03:53.626  LOG <examples> INFO: Cleanup node: three_viw9g9
2018-07-02 11:03:53.626  LOG <examples> INFO: Cleanup node: four_v7m6nk
Execution ended, waiting 3 seconds for additional log messages
2018-07-02 11:03:54.632  LOG <examples> INFO: Cleanup node: two_05vh0m
2018-07-02 11:03:54.632  LOG <examples> INFO: Cleanup node: six_qyg6ll
2018-07-02 11:03:54.746  CFY <examples> 'scaledownlist' workflow execution succeeded
Finished executing workflow scaledownlist on deployment examples
* Run 'cfy events list -e dcf53181-19e2-439c-b052-42b01b62557a' to retrieve the execution's events/logs
```

State after:
```shell
$ cfy node-instances get two_05vh0m
Retrieving node instance two_05vh0m

Node-instance:
+------------+---------------+---------+---------+---------------+------------+----------------+------------+
|     id     | deployment_id | host_id | node_id |     state     | visibility |  tenant_name   | created_by |
+------------+---------------+---------+---------+---------------+------------+----------------+------------+
| two_05vh0m |    examples   |         |   two   | uninitialized |   tenant   | default_tenant |   admin    |
+------------+---------------+---------+---------+---------------+------------+----------------+------------+

Instance runtime properties:
```

## Remove instances created by install workflow without transaction id

Remove instances [without transaction id](examples/scaledown_without_transaction.yaml).
```shell
$ cfy executions start scaledownlist -d examples -p cloudify-utilities-plugin/cloudify_scalelist/examples/scaledown_without_transaction.yaml
Executing workflow scaledownlist on deployment examples [timeout=900 seconds]
2018-07-03 10:34:15.991  CFY <examples> Starting 'scaledownlist' workflow execution
2018-07-03 10:34:16.682  LOG <examples> INFO: Scale rules: {u'one': {'count': 1, 'values': [u'one_eayebr']}}
2018-07-03 10:34:16.682  LOG <examples> INFO: Scale down u'one' by delta: 1
2018-07-03 10:34:16.682  LOG <examples> INFO: Scale settings: {u'one': {'instances': 0, 'removed_ids_include_hint': [u'one_eayebr']}}
2018-07-03 10:34:16.682  LOG <examples> INFO: Deployment modification started. [modification_id=47d4bc5b-2704-41c8-9187-dd2c5e4d0411]
2018-07-03 10:34:16.682  LOG <examples> INFO: Proposed: [u'one_eayebr']
2018-07-03 10:34:16.682  LOG <examples> INFO: Removed: [u'one_eayebr']
2018-07-03 10:34:16.670  CFY <examples> [one_eayebr] Stopping node
2018-07-03 10:34:17.676  CFY <examples> [one_eayebr] Deleting node
2018-07-03 10:34:17.676  CFY <examples> [one_eayebr.delete] Sending task 'script_runner.tasks.run'
2018-07-03 10:34:17.676  CFY <examples> [one_eayebr.delete] Task started 'script_runner.tasks.run'
2018-07-03 10:34:18.265  LOG <examples> [one_eayebr.delete] INFO: Downloaded scripts/delete.py to /tmp/PKZZQ/tmpQ7dTgb-delete.py
2018-07-03 10:34:18.688  LOG <examples> [one_eayebr.delete] INFO: We have some resource u'one_eayebr', so we can delete such
2018-07-03 10:34:18.688  LOG <examples> [one_eayebr.delete] INFO: Resulted properties: {u'predefined': u'', u'resource_name': u'one0', u'defined_in_inputs': u'', u'resource_id': u'one_eayebr', 'ctx': <cloudify.context.CloudifyContext object at 0x3536390>, u'_transaction_id': u'', u'script_path': u'scripts/delete.py'}
2018-07-03 10:34:18.679  CFY <examples> [one_eayebr.delete] Task succeeded 'script_runner.tasks.run'
2018-07-03 10:34:19.685  CFY <examples> 'scaledownlist' workflow execution succeeded
Finished executing workflow scaledownlist on deployment examples
* Run 'cfy events list -e 715e3f97-07d5-4052-8879-aefa4e536a2c' to retrieve the execution's events/logs
```

## Remove any instance by field value and ignore transaction

Remove instances [without transaction and field value](examples/scaledown_byvalue.yaml).

```shell
$ cfy executions start scaledownlist -d examples -p cloudify-utilities-plugin/cloudify_scalelist/examples/scaledown_byvalue.yaml
Executing workflow scaledownlist on deployment examples [timeout=900 seconds]
2018-07-03 15:33:43.106  CFY <examples> Starting 'scaledownlist' workflow execution
2018-07-03 15:33:43.686  LOG <examples> INFO: Scale rules: {u'two_scale': {'count': 1, 'values': [u'two_d8hmqx']}}
2018-07-03 15:33:43.686  LOG <examples> INFO: Scale down u'two_scale' by delta: 1
2018-07-03 15:33:43.686  LOG <examples> INFO: Scale settings: {u'two_scale': {'instances': 2, 'removed_ids_include_hint': [u'two_d8hmqx']}}
2018-07-03 15:33:43.686  LOG <examples> INFO: Deployment modification started. [modification_id=6f7020a1-7e6b-402f-912d-124dc7a4fcfd]
2018-07-03 15:33:43.686  LOG <examples> INFO: Removed: [u'two_ln2tgh']
2018-07-03 15:33:43.686  LOG <examples> WARNING: Rolling back deployment modification. [modification_id=6f7020a1-7e6b-402f-912d-124dc7a4fcfd]: Exception("Instance u'two_ln2tgh' not in proposed list [u'two_d8hmqx'].",)
2018-07-03 15:33:43.686  LOG <examples> INFO: Proposed: [u'two_d8hmqx']
2018-07-03 15:33:44.696  LOG <examples> INFO: Scale down based on transaction failed: Exception("Instance u'two_ln2tgh' not in proposed list [u'two_d8hmqx'].",)
2018-07-03 15:33:44.214  CFY <examples> [two_d8hmqx] Stopping node
2018-07-03 15:33:45.237  CFY <examples> [two_d8hmqx] Deleting node
2018-07-03 15:33:45.237  CFY <examples> [two_d8hmqx.delete] Sending task 'script_runner.tasks.run'
2018-07-03 15:33:45.237  CFY <examples> [two_d8hmqx.delete] Task started 'script_runner.tasks.run'
2018-07-03 15:33:46.032  LOG <examples> [two_d8hmqx.delete] INFO: Downloaded scripts/delete.py to /tmp/O5YRB/tmpI_9Fux-delete.py
2018-07-03 15:33:46.701  LOG <examples> [two_d8hmqx.delete] INFO: Resulted properties: {u'predefined': u'', u'resource_name': u'two1', u'defined_in_inputs': u'one_saqz5k', u'resource_id': u'two_d8hmqx', 'ctx': <cloudify.context.CloudifyContext object at 0x25ba390>, u'_transaction_id': u'e919969a-af7a-494f-8b9b-f0712833c133', u'script_path': u'scripts/delete.py'}
2018-07-03 15:33:46.701  LOG <examples> [two_d8hmqx.delete] INFO: We have some resource u'two_d8hmqx', so we can delete such
2018-07-03 15:33:46.255  CFY <examples> [two_d8hmqx.delete] Task succeeded 'script_runner.tasks.run'
2018-07-03 15:33:46.701  LOG <examples> INFO: Cleanup node: two_d8hmqx
2018-07-03 15:33:46.689  CFY <examples> 'scaledownlist' workflow execution succeeded
Finished executing workflow scaledownlist on deployment examples
* Run 'cfy events list -e 93c72e69-2ce7-411f-9121-9d0c2ba53852' to retrieve the execution's events/logs
```

## Run update on instances by field name, field value and node name.

Run [update action](examples/update_params.yaml) for specific by property value on node 'two'.

```shell
$ cfy executions start update_operation_filtered -d examples -p cloudify-utilities-plugin/cloudify_scalelist/examples/update_params.yaml
Executing workflow update_operation_filtered on deployment examples [timeout=900 seconds]
2018-07-06 14:37:31.066  CFY <examples> Starting 'update_operation_filtered' workflow execution
2018-07-06 14:37:32.000  CFY <examples> [two_4r9k30] Starting operation cloudify.interfaces.lifecycle.update (Operation parameters: {u'check': True})
2018-07-06 14:37:32.000  CFY <examples> [two_4r9k30.update] Sending task 'script_runner.tasks.run'
2018-07-06 14:37:32.000  CFY <examples> [two_4r9k30.update] Task started 'script_runner.tasks.run'
2018-07-06 14:37:32.461  LOG <examples> [two_4r9k30.update] INFO: Downloaded scripts/update.py to /tmp/NILXD/update.py
2018-07-06 14:37:32.461  LOG <examples> [two_4r9k30.update] INFO: Resulted properties: {u'predefined': u'', u'resource_name': u'two0', u'_transaction_id': u'two_precreated', u'resource_id': u'two_4r9k30', u'script_path': u'scripts/update.py', 'ctx': <cloudify.context.CloudifyContext object at 0x7f4f86b72150>, u'check': True}
2018-07-06 14:37:33.003  CFY <examples> [two_4r9k30.update] Task succeeded 'script_runner.tasks.run'
2018-07-06 14:37:34.006  CFY <examples> [two_4r9k30] Finished operation cloudify.interfaces.lifecycle.update
2018-07-06 14:37:34.006  CFY <examples> 'update_operation_filtered' workflow execution succeeded
Finished executing workflow update_operation_filtered on deployment examples
* Run 'cfy events list -e 7f5231e7-e440-4378-ada1-9088fa405532' to retrieve the execution's events/logs
```

## Remove instances from DB

Run on manager for enable DB cleanup on manager:

* Enable ability to run scripts from `cfyuser` with `sudo`.
```shell
$ sudo su -c "echo '' >> /etc/sudoers.d/cfyuser"
$ sudo su -c "echo 'cfyuser ALL=(ALL) NOPASSWD:/opt/manager/env/bin/python' >> /etc/sudoers.d/cfyuser"
```
* Copy `cloudify_scalelist/examples/scripts/cleanup_deployments.py` to
`/opt/manager/scripts/`.
* Use `scaledownlist` with `force_db_cleanup`==`True`.
