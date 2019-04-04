# Introduction

Blueprint handles operations with Infoblox objects.

# Overview

Blueprint provides example for create cname, a/ptr records and register host
with ip from created network. Implementation based on
[rest plugin](https://github.com/cloudify-incubator/cloudify-utilities-plugin/blob/master/cloudify_rest/README.md)
and
[rest template](https://github.com/cloudify-incubator/cloudify-utilities-plugins-sdk#rest-yaml-template-format).

Code is based on
[Infoblox API](https://www.infoblox.com/wp-content/uploads/infoblox-deployment-infoblox-rest-api.pdf)
and checked with NIOS 8.3.1.

Infoblox trial version can be downloaded from [DDI](https://info.infoblox.com/WW_FY17_OS_PE_OrganicGlossary-DDI).

# Blueprint Requirements

* Rest plugin:
    * cloudify-utilities-plugin >= 1.12.3
* Infoblox:
    * NIOS >= 8.3.1

# Types

Defined in [Infoblox types](infoblox.yaml)

## `infoblox.record_a` Create a record

Properties:
* `hosts`: list of hosts name or IP addresses of Rest Servers
* `host`: host name or IP addresses of Rest Servers if list of hosts is not
  needed single host can be provided by this property. NOTE: the 'hosts'
  property overwirte the 'host' property
* `port`: port number. When -1 default ports are used (80 for ssl = false
  and 443 for ssl = true). Default: -1
* `ssl`: http or https. Default: `false`
* `verify`: A boolean which controls whether we verify the server's TLS
  certificate. Default: `true`
* `record`: A record properties
  * `ipv4addr`: ip v4 address.
  * `name`: record name

## `infoblox.update_record_a` update precreted a record

Properties:
* `hosts`: list of hosts name or IP addresses of Rest Servers
* `host`: host name or IP addresses of Rest Servers if list of hosts is not
  needed single host can be provided by this property. NOTE: the 'hosts'
  property overwirte the 'host' property
* `port`: port number. When -1 default ports are used (80 for ssl = false
  and 443 for ssl = true). Default: -1
* `ssl`: http or https. Default: `false`
* `verify`: A boolean which controls whether we verify the server's TLS
  certificate. Default: `true`
* `record`: A record properties
  * `ipv4addr`: new ip v4 address.
  * `name`: record name

## `infoblox.record_ptr` Create ptr record

Properties:
* `hosts`: list of hosts name or IP addresses of Rest Servers
* `host`: host name or IP addresses of Rest Servers if list of hosts is not
  needed single host can be provided by this property. NOTE: the 'hosts'
  property overwirte the 'host' property
* `port`: port number. When -1 default ports are used (80 for ssl = false
  and 443 for ssl = true). Default: -1
* `ssl`: http or https. Default: `false`
* `verify`: A boolean which controls whether we verify the server's TLS
  certificate. Default: `true`
* `record`: A record properties
  * `ipv4addr`: ip v4 address.
  * `name`: record name

## `infoblox.record_host` Create host

Properties:
* `hosts`: list of hosts name or IP addresses of Rest Servers
* `host`: host name or IP addresses of Rest Servers if list of hosts is not
  needed single host can be provided by this property. NOTE: the 'hosts'
  property overwirte the 'host' property
* `port`: port number. When -1 default ports are used (80 for ssl = false
  and 443 for ssl = true). Default: -1
* `ssl`: http or https. Default: `false`
* `verify`: A boolean which controls whether we verify the server's TLS
  certificate. Default: `true`
* `record`: A record properties
  * `ipv4addr`: ip v4 address.
  * `name`: host name

## `infoblox.update_host` update precreted host record

Properties:
* `hosts`: list of hosts name or IP addresses of Rest Servers
* `host`: host name or IP addresses of Rest Servers if list of hosts is not
  needed single host can be provided by this property. NOTE: the 'hosts'
  property overwirte the 'host' property
* `port`: port number. When -1 default ports are used (80 for ssl = false
  and 443 for ssl = true). Default: -1
* `ssl`: http or https. Default: `false`
* `verify`: A boolean which controls whether we verify the server's TLS
  certificate. Default: `true`
* `record`: A record properties
  * `ipv4addr`: new ip v4 address.
  * `name`: host name

## `infoblox.record_network` Create network

Properties:
* `hosts`: list of hosts name or IP addresses of Rest Servers
* `host`: host name or IP addresses of Rest Servers if list of hosts is not
  needed single host can be provided by this property. NOTE: the 'hosts'
  property overwirte the 'host' property
* `port`: port number. When -1 default ports are used (80 for ssl = false
  and 443 for ssl = true). Default: -1
* `ssl`: http or https. Default: `false`
* `verify`: A boolean which controls whether we verify the server's TLS
  certificate. Default: `true`
* `network`: A network properties
  * `addr`: ip v4 addresses set.

## `infoblox.request_free_ips` get free ips from network

Properties:
* `hosts`: list of hosts name or IP addresses of Rest Servers
* `host`: host name or IP addresses of Rest Servers if list of hosts is not
  needed single host can be provided by this property. NOTE: the 'hosts'
  property overwirte the 'host' property
* `port`: port number. When -1 default ports are used (80 for ssl = false
  and 443 for ssl = true). Default: -1
* `ssl`: http or https. Default: `false`
* `verify`: A boolean which controls whether we verify the server's TLS
  certificate. Default: `true`
* `network`: A network properties
  * `addr`: ip v4 addresses set/network name.
  * `amount`: count of ip for get

# Example Blueprints:

## [Minimal blueprint](example-infoblox-blueprint.yaml)

### Inputs:
* `rest_endpoint`: Infoblox ip
* `rest_username`: Infoblox username
* `rest_userpass`: Infoblox password
* `record_network_addrs`: Network addreses with netmask, e.g.: `10.0.0.0/24`
* `record_host_name`: New a record/host name

### Implemented nodes:
* `network_record`: Create/Delete network
* `network_ids_record`: Get network state and ask about several unassigned ip
* `a_record`: Create/Delete a record
* `ptr_record`: Create/Delete ptr record
* `host_record`: Create/Delete hos record
* `update_host`: Get host and update record information
* `update_records` Get a record and update with new information
