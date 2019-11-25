Weave
=======

Weave 2.0.1 is supported by kubespray

Weave uses [**consensus**](https://www.weave.works/docs/net/latest/ipam/##consensus) mode (default mode) and [**seed**](https://www.weave.works/docs/net/latest/ipam/#seed) mode.

`Consensus` mode is best to use on static size cluster and `seed` mode is best to use on dynamic size cluster

Weave encryption is supported for all communication

* To use Weave encryption, specify a strong password (if no password, no encryption)

```
# In file ./inventory/sample/group_vars/k8s-cluster.yml
weave_password: EnterPasswordHere
```

This password is used to set an environment variable inside weave container.

Weave is deployed by kubespray using a daemonSet

* Check the status of Weave containers

```
# From client
kubectl -n kube-system get pods | grep weave
# output
weave-net-50wd2                       2/2       Running   0          2m
weave-net-js9rb                       2/2       Running   0          2m
```
There must be as many pods as nodes (here kubernetes have 2 nodes so there are 2 weave pods).

* Check status of weave (connection,encryption ...) for each node

```
# On nodes
curl http://127.0.0.1:6784/status
# output on node1
Version: 2.0.1 (up to date; next check at 2017/08/01 13:51:34)

        Service: router
       Protocol: weave 1..2
           Name: fa:16:3e:b3:d6:b2(node1)
     Encryption: enabled
  PeerDiscovery: enabled
        Targets: 2
    Connections: 2 (1 established, 1 failed)
          Peers: 2 (with 2 established connections)
 TrustedSubnets: none

        Service: ipam
         Status: ready
          Range: 10.233.64.0/18
  DefaultSubnet: 10.233.64.0/18
```

* Check parameters of weave for each node

```
# On nodes
ps -aux | grep weaver
# output on node1 (here its use seed mode)
root      8559  0.2  3.0 365280 62700 ?        Sl   08:25   0:00 /home/weave/weaver --name=fa:16:3e:b3:d6:b2 --port=6783 --datapath=datapath --host-root=/host --http-addr=127.0.0.1:6784 --status-addr=0.0.0.0:6782 --docker-api= --no-dns --db-prefix=/weavedb/weave-net --ipalloc-range=10.233.64.0/18 --nickname=node1 --ipalloc-init seed=fa:16:3e:b3:d6:b2,fa:16:3e:f0:50:53 --conn-limit=30 --expect-npc 192.168.208.28 192.168.208.19
```

### Consensus mode (default mode)

This mode is best to use on static size cluster

### Seed mode

This mode is best to use on dynamic size cluster

The seed mode also allows multi-clouds and hybrid on-premise/cloud clusters deployement.

* Switch from consensus mode to seed mode

```
# In file ./inventory/sample/group_vars/k8s-cluster.yml
weave_mode_seed: true
```

These two variables are only used when `weave_mode_seed` is set to `true` (**/!\ do not manually change these values**)

```
# In file ./inventory/sample/group_vars/k8s-cluster.yml
weave_seed: uninitialized
weave_peers: uninitialized
```

The first variable, `weave_seed`, contains the initial nodes of the weave network

The second variable, `weave_peers`, saves the IPs of all nodes joined to the weave network

These two variables are used to connect a new node to the weave network. The new node needs to know the firsts nodes (seed) and the list of IPs of all nodes.

To reset these variables and reset the weave network set them to `uninitialized`
