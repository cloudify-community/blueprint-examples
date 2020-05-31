# Cloudify Utilities: Cloud-Init

Cloud-Init is the standard for configuration of cloud instances. See
[examples](http://cloudinit.readthedocs.io/en/latest/topics/examples.html).

# external files/jinja2 templates in write_files.content

To use files from blueprint directory as tempate for files in `write_files`
(content resource_config -> write_files -> content), it has to be defined as
a dictionary which may contain three keys:
* `resource_type`: if it's filled with string "file_resource", the plugin
will be looking for resources under the path defined in `resource_name`,
* `resource_name`: defines the path, where the resource resides,
* `template_variables`: if not empty, this dictionary is being used to fill
the resource content (jinja2 template) with variables.

Combined configuration can be used by `cloud_config` as yaml text or `json_config` as json text.

```
  cloud_init_image:
    ....
    interfaces:
      cloudify.interfaces.lifecycle:
        create:
          inputs:
            ....
            vol_ident: config-2
            files:
              # meta
              "openstack/latest/meta_data.json": { get_attribute: [meta_data_init, json_config ] }
              # vendor
              "openstack/latest/vendor_data.json": { get_attribute: [vendor_data_init, json_config ] }
              # https://cloudbase-init.readthedocs.io/en/latest/userdata.html
              "openstack/latest/user_data": { get_attribute: [user_data_init, cloud_config ] }
    relationships:
    - target: user_data_init
      type: cloudify.relationships.depends_on
    - target: meta_data_init
      type: cloudify.relationships.depends_on
    - target: vendor_data_init
      type: cloudify.relationships.depends_on
```

# Cloudinit example

For more info look to [documentation](https://cloudinit.readthedocs.io/en/latest/topics/datasources/nocloud.html)

```
  cloud_init_user:
    type: cloudify.nodes.CloudInit.CloudConfig
    interfaces:
      cloudify.interfaces.lifecycle:
        create:
          inputs:
            resource_config:
              users:
              - name: centos
                primary_group: centos
                # mkpasswd --method=SHA-512 --rounds=4096
                # hash of passw0rd
                passwd: $6$rounds=4096$sEbWYCRnr$kV18TY9O9Bkq0DdSo5Zvp8saK0gnpZ3RD.55YvQp1ZuaU89eG/T3UrWRh7s9SzchEjebL9ETr2KyMVHqtiXbQ.
                groups: users, admin, wheel
                lock_passwd: false
                shell: /bin/bash
                sudo: ['ALL=(ALL) NOPASSWD:ALL']
                ssh_authorized_keys:
                - { get_attribute: [agent_key, public_key_export] }
              growpart:
                mode: auto
                devices: ['/']
                ignore_growroot_disabled: false
              packages:
              - [epel-release]
              - [deltarpm]
              write_files:
              - path: /etc/yum.repos.d/custom.repo
                content: |
                  [local_base]
                  name=Custom Repository
                  baseurl=http://localhost:8080/base/
                  enabled=0
                  gpgcheck=0
```

# Cloudbase-init example

For more info look to [documentation](https://cloudbase-init.readthedocs.io/en/latest/userdata.html)

```
  user_data_init:
    type: cloudify.nodes.CloudInit.CloudConfig
    properties:
      resource_config:
        users:
          - name: cloudify
            gecos: 'Cloudify Agent User'
            primary_group: Users
            groups: Administrators
            passwd: { get_input: cloudify_password }
            inactive: False
            expiredate: "2020-10-01"
        write_files:
        - content:
            resource_type: file_resource
            resource_name: scripts/domain.ps1
            template_variables:
              DC_IP: { get_input: cloudify_dc_ip }
              DC_NAME: { get_input: cloudify_dc_name }
              DC_PASSWORD: { get_input: cloudify_dc_password }
          path: C:\domain.ps1
          permissions: '0644'
        runcmd:
        - 'powershell.exe C:\\domain.ps1'
```
