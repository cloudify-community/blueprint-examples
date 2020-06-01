# Cloudify Utilities: REST plugin

## Description
The purpose of this plugin is to provide a generic type in a blueprint in order
to integrate with REST based systems. The plugin is suitable for REST API's which
expose a relatively high level of abstraction. The general concept is to use JINJA
templates that will be evaluated as the content of several independent REST calls.
Very often it happens that certian intent requires several REST calls - therefore
we can put them in a single template to make blueprint much cleaner to read.

Features:

- JINJA templates
- selective update of runtime properties with REST response content
- configurable recoverable errors
- context sensitive "response expectation"

Before executing those examples, its strongly recommended read the full documentation
 [here.](https://github.com/cloudify-incubator/cloudify-utilities-plugin/blob/master/cloudify_rest/README.md) 

### Examples

blueprint: [example-1-blueprint.yaml](./example-1-blueprint.yaml)

The example is a REST API from test website: https://jsonplaceholder.typicode.com/.

The purpose of blueprint is to demonstrate how **response_translation** work.

For example, suppose that you were to use a simple GET call, such as:

`GET https://jsonplaceholder.typicode.com/users/10**`

This returns the following JSON:

```json
{
    "id": 10,
    "name": "Clementina DuBuque",
    "username": "Moriah.Stanton",
    "email": "Rey.Padberg@karina.biz",
    "address": {
        "street": "Kattie Turnpike",
        "suite": "Suite 198",
        "city": "Lebsackbury",
        "zipcode": "31428-2261",
        "geo": {
            "lat": "-38.2386",
            "lng": "57.2232"
        }
    },
    "phone": "024-648-3804",
    "website": "ambrose.net",
    "company": {
        "name": "Hoeger LLC",
        "catchPhrase": "Centralized empowering task-force",
        "bs": "target end-to-end models"
    }
}
```

In the blueprint there are two nodes:

  * user10-all-properties - in this node we'will put complete response under
    **user** runtime property
  * user10-some-properties - in this node we'll selectively put response values
    under given keys

```shell
(cfy-4.2) $ cfy node-instances list
Listing all instances...

Node-instances:
+-------------------------------+---------------+---------+------------------------+---------+--------------+----------------+------------+
|               id              | deployment_id | host_id |        node_id         |  state  | availability |  tenant_name   | created_by |
+-------------------------------+---------------+---------+------------------------+---------+--------------+----------------+------------+
|  user10-all-properties_31b1sn |    example    |         | user10-all-properties  | started |    tenant    | default_tenant |   admin    |
| user10-some-properties_jbckbv |    example    |         | user10-some-properties | started |    tenant    | default_tenant |   admin    |
+-------------------------------+---------------+---------+------------------------+---------+--------------+----------------+------------+

(cfy-4.2) rest-plugin-examples$ cfy node-instances get user10-all-properties_31b1sn
Retrieving node instance user10-all-properties_31b1sn

Node-instance:
+------------------------------+---------------+---------+-----------------------+---------+--------------+----------------+------------+
|              id              | deployment_id | host_id |        node_id        |  state  | availability |  tenant_name   | created_by |
+------------------------------+---------------+---------+-----------------------+---------+--------------+----------------+------------+
| user10-all-properties_31b1sn |    example    |         | user10-all-properties | started |    tenant    | default_tenant |   admin    |
+------------------------------+---------------+---------+-----------------------+---------+--------------+----------------+------------+

Instance runtime properties:
    user: {'username': 'Moriah.Stanton', 'website': 'ambrose.net', 'name': 'Clementina DuBuque', 'company': {'bs': 'target end-to-end models', 'catchPhrase': 'Centralized empowering task-force', 'name': 'Hoeger LLC'}, 'id': 10, 'phone': '024-648-3804', 'address': {'suite': 'Suite 198', 'street': 'Kattie Turnpike', 'geo': {'lat': '-38.2386', 'lng': '57.2232'}, 'zipcode': '31428-2261', 'city': 'Lebsackbury'}, 'email': 'Rey.Padberg@karina.biz'}

(cfy-4.2) rest-plugin-examples$ cfy node-instances get user10-some-properties_jbckbv
Retrieving node instance user10-some-properties_jbckbv

Node-instance:
+-------------------------------+---------------+---------+------------------------+---------+--------------+----------------+------------+
|               id              | deployment_id | host_id |        node_id         |  state  | availability |  tenant_name   | created_by |
+-------------------------------+---------------+---------+------------------------+---------+--------------+----------------+------------+
| user10-some-properties_jbckbv |    example    |         | user10-some-properties | started |    tenant    | default_tenant |   admin    |
+-------------------------------+---------------+---------+------------------------+---------+--------------+----------------+------------+

Instance runtime properties:
    user-city-zip: 31428-2261
    user-email: Rey.Padberg@karina.biz
    user-city-geo: {'latitude': '-38.2386', 'longnitude': '57.2232'}
    user-full-name: Clementina DuBuque
    user-city: Lebsackbury

(cfy-4.2) rest-plugin-examples$

```

**Notes**:

* Please provide 'cacert_bundle' secret from a file:

Ubuntu, usually at: "/usr/lib/python2.7/dist-packages/certifi/cacert.pem"

Centos, usually at: "/opt/manager/env/lib/python2.7/site-packages/certifi/cacert.pem"

Example for centos:

`cfy secrets create -f /opt/manager/env/lib/python2.7/site-packages/certifi/cacert.pem cacert_bundle`

* Use /inputs/rest_endpoint_cert.yaml as input.

`cfy install example-1-blueprint.yaml  -i ./inputs/rest_endpoint_cert.yaml`

### Example 2

blueprint: [example-2-blueprint.yaml](./example-2-blueprint.yaml)

Same as above we're using test REST API but this time we'll demonstrate how we
can combine multiple REST calls in a single template. Overall idea is that
we'll first query REST API to provide user details and later on we'll use this
details in order to create user post with POST method.


### Example 3

blueprint: [example-3-blueprint.yaml](./example-3-blueprint.yaml)

Real life example how F5 BigIP can be provisioned with REST API.
Creates 2 VLAN's(1.1,1.2) and associates an ip to each of them.
Provide managment_ip, user_name and password inputs.

Example:

`cfy install example-3-blueprint.yaml -i mgmt_ip=<ip> -i username=<username> -i password=<password> `

### Example 4 
blueprint: [example-4-blueprint.yaml](./example-4-blueprint.yaml)

Example of get commit details on github using github api.

The repository to get the commit from is the [cloudify utillities plugin.](https://github.com/cloudify-incubator/cloudify-utilities-plugin)

Provide commit sha as an input.

Example:

cfy install example-4-blueprint.yaml -i commit=<commit_sha>

### Example 5

blueprint: [example-5-blueprint.yaml](./example-5-blueprint.yaml)

Example for get users list, create new user based on first result and than
remove new created user. Have used `cloudify.rest.BunchRequests` with
`params_attributes`.

### Example 6

blueprint: [example-6-blueprint.yaml](./example-6-blueprint.yaml)

This example demonstrates get user details and store only selected parts of response under distinct runtime properties.

### Example 7

blueprint: [example-7-blueprint.yaml](./example-7-blueprint.yaml)

This example demonstrates create users with 3 different ways to load the user properties(request payload)

### Example 8

blueprint: [example-8-blueprint.yaml](./example-8-blueprint.yaml)

This example demonstrates 2 requests, firstly get user and save it in runtime properties,
than execute PUT request and change the user details.

### Example 9

blueprint: [example-9-blueprint.yaml](./example-9-blueprint.yaml)

This example perform the same as the previous example but seperate the GET operation and PUT operation into two different templates.
After getting the user it saves it as runtime property and uses it for the PUT call.

### Example github-status

blueprint: [example-github-status.yaml](./example-github-status.yaml)

This example perform GET request in order to get the github status.