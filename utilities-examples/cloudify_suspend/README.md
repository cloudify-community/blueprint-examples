# Cloudify Utilities: Suspend
Additional suport for `suspend`, `resume`, `backup`, `restore`, `remove_backup`
workflows.

For more information read the [documentation](https://github.com/cloudify-incubator/cloudify-utilities-plugin/blob/master/cloudify_suspend/README.md).

# example:

1. Upload the [blueprint](./example.yaml) :

`cfy blueprints upload example.yaml `

2. Create deployment: 
`cfy deployments create -b cloudify-suspend`
3. Call 'suspend' workflow:

Suspend:

```shell
$ cfy execution start suspend -d cloudify-suspend 
Executing workflow `suspend` on deployment `cloudify-suspend` [timeout=900 seconds]
2020-05-27 14:06:39.552  CFY <cloudify-suspend> Starting 'suspend' workflow execution
2020-05-27 14:06:39.556  CFY <cloudify-suspend> [server_0chf3l] Starting to cloudify.interfaces.lifecycle.suspend
2020-05-27 14:06:39.821  CFY <cloudify-suspend> [server_0chf3l.suspend] Sending task 'script_runner.tasks.run'
2020-05-27 14:06:41.641  LOG <cloudify-suspend> [server_0chf3l.suspend] INFO: Downloaded scripts/suspend.py to /tmp/3VLF5/suspend.py
2020-05-27 14:06:41.701  LOG <cloudify-suspend> [server_0chf3l.suspend] INFO: suspend server_id=Server!
2020-05-27 14:06:42.420  CFY <cloudify-suspend> [server_0chf3l.suspend] Task succeeded 'script_runner.tasks.run'
2020-05-27 14:06:42.523  CFY <cloudify-suspend> [server_0chf3l] Done cloudify.interfaces.lifecycle.suspend
2020-05-27 14:06:42.692  CFY <cloudify-suspend> 'suspend' workflow execution succeeded

```
4. call `resume` workflow:
```shell
$ cfy execution start resume -d cloudify-suspend 
Executing workflow `resume` on deployment `cloudify-suspend` [timeout=900 seconds]
2020-05-27 14:06:08.910  CFY <cloudify-suspend> Starting 'resume' workflow execution
2020-05-27 14:06:08.915  CFY <cloudify-suspend> [server_0chf3l] Starting to cloudify.interfaces.lifecycle.resume
2020-05-27 14:06:09.179  CFY <cloudify-suspend> [server_0chf3l.resume] Sending task 'script_runner.tasks.run'
2020-05-27 14:06:10.970  LOG <cloudify-suspend> [server_0chf3l.resume] INFO: Downloaded scripts/resume.py to /tmp/TXFUE/resume.py
2020-05-27 14:06:11.044  LOG <cloudify-suspend> [server_0chf3l.resume] INFO: resume server_id=Server!
2020-05-27 14:06:11.773  CFY <cloudify-suspend> [server_0chf3l.resume] Task succeeded 'script_runner.tasks.run'
2020-05-27 14:06:11.787  CFY <cloudify-suspend> [server_0chf3l] Done cloudify.interfaces.lifecycle.resume
2020-05-27 14:06:11.957  CFY <cloudify-suspend> 'resume' workflow execution succeeded

```



## More executions logs:

Create backup:

```shell
$ cfy executions start backup -d examples -p snapshot_name=backup_example --task-retry-interval 30 --task-retries 30
2018-05-16 12:10:22.408  CFY <examples> Starting 'backup' workflow execution
2018-05-16 12:10:22.413  CFY <examples> [example_node_s4bgna] Starting to cloudify.interfaces.freeze.fs_prepare
2018-05-16 12:10:22.413  CFY <examples> [qemu_vm_jvv6jt] Starting to cloudify.interfaces.snapshot.create
2018-05-16 12:10:22.413  CFY <examples> [example_node_s4bgna] Starting to cloudify.interfaces.freeze.fs_finalize
2018-05-16 12:10:22.512  CFY <examples> [example_node_s4bgna.fs_finalize] Sending task 'cloudify_terminal.tasks.run'
2018-05-16 12:10:22.512  CFY <examples> [qemu_vm_jvv6jt.create] Sending task 'cloudify_libvirt.domain_tasks.snapshot_create'
...
2018-05-16 12:10:47.604  CFY <examples> [example_node_s4bgna] Done cloudify.interfaces.freeze.fs_finalize
2018-05-16 12:10:47.604  CFY <examples> [qemu_vm_jvv6jt] Done cloudify.interfaces.snapshot.create
2018-05-16 12:10:47.681  CFY <examples> [example_node_s4bgna] Done cloudify.interfaces.freeze.fs_prepare
2018-05-16 12:10:47.767  LOG <examples> INFO: Backuped to u'backup_example'
2018-05-16 12:10:47.768  CFY <examples> 'backup' workflow execution succeeded
```

Restore backup:

```shell
$ cfy executions start restore -d examples -p snapshot_name=backup_example --task-retry-interval 30 --task-retries 30
2018-05-16 12:12:43.913  CFY <examples> Starting 'restore' workflow execution
2018-05-16 12:12:43.917  CFY <examples> [example_node_s4bgna] Starting to cloudify.interfaces.freeze.fs_finalize
2018-05-16 12:12:43.917  CFY <examples> [qemu_vm_jvv6jt] Starting to cloudify.interfaces.snapshot.apply
2018-05-16 12:12:43.917  CFY <examples> [example_node_s4bgna] Starting to cloudify.interfaces.freeze.fs_prepare
...
2018-05-16 12:13:13.114  CFY <examples> [example_node_s4bgna] Done cloudify.interfaces.freeze.fs_prepare
2018-05-16 12:13:13.229  CFY <examples> [example_node_s4bgna] Done cloudify.interfaces.freeze.fs_finalize
2018-05-16 12:13:13.314  LOG <examples> INFO: Restored from u'backup_example'
2018-05-16 12:13:13.314  CFY <examples> 'restore' workflow execution succeeded
```

Delete backup:

```shell
$ cfy executions start remove_backup -d examples -p snapshot_name=backup_example --task-retry-interval 30 --task-retries 30
2018-05-16 12:14:42.171  CFY <examples> Starting 'remove_backup' workflow execution
2018-05-16 12:14:42.174  CFY <examples> [qemu_vm_jvv6jt] Starting to cloudify.interfaces.snapshot.delete
2018-05-16 12:14:42.275  CFY <examples> [qemu_vm_jvv6jt.delete] Sending task 'cloudify_libvirt.domain_tasks.snapshot_delete'
2018-05-16 12:14:42.322  CFY <examples> [qemu_vm_jvv6jt.delete] Task started 'cloudify_libvirt.domain_tasks.snapshot_delete'
2018-05-16 12:14:42.364  LOG <examples> [qemu_vm_jvv6jt.delete] INFO: remove_backup
2018-05-16 12:14:42.429  LOG <examples> [qemu_vm_jvv6jt.delete] INFO: Backup deleted: vm-backup_example
2018-05-16 12:14:42.430  CFY <examples> [qemu_vm_jvv6jt.delete] Task succeeded 'cloudify_libvirt.domain_tasks.snapshot_delete'
2018-05-16 12:14:42.499  CFY <examples> [qemu_vm_jvv6jt] Done cloudify.interfaces.snapshot.delete
2018-05-16 12:14:42.578  LOG <examples> INFO: Removed u'backup_example'
2018-05-16 12:14:42.578  CFY <examples> 'remove_backup' workflow execution succeeded
```
