# ansbile-install-uninstall

set of examples to leverage ansible playbook , on container create and on stop execute another playbook

**NOTE** about blueprint_packed_image.yaml inside ansbile directory you need to do

```shell
dokcer build -t ansible_local:0.1 .
```

and you can modify docker_config as well , it is using local sock protocol.