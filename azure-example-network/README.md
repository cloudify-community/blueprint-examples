# Azure Example Network

### Resources Created

  * `resource_group`
  * `network`
  * `subnet`


## Compatibility

Tested with:
  * Cloudify 4.5.5


## Pre-installation steps

Upload the required plugins:

  * [Azure Plugin](https://github.com/cloudify-cosmo/cloudify-azure-plugin/releases), version 2.1.1 or higher.

_Check the blueprint for the exact version of the plugin._

You must have these secrets on your Cloudify Manager `tenant`:

  * `subscription_id`: Your Azure subscription ID.
  * `tenant_id`: Your Azure Active Directory Service Principal tenant ID.
  * `client_id`: Your Azure Active Directory Service Principal client ID (appId).
  * `client_secret`: Your Azure Active Directory Service Principal client secret (password).
  * `location`: Any valid Azure location, such as `eastus`.

**You may override the secrets' values via deployment inputs when you create the deployment.**


## Installation

1. On your Cloudify Manager, navigate to `Local Blueprints` and select `Upload`. [Right-click and copy URL](https://github.com/cloudify-community/blueprint-examples/archive/master.zip). Paste where it says `Enter blueprint url`. Provide a blueprint name, such as `azure-example-blueprint` in the field labeled `blueprint name`. Select `azure-example-network/blueprint.yaml` from `Blueprint filename` menu.

1. After the new blueprint has been created, click the `Deploy` button.

1. Navigate to `Deployments`, find your new deployment, select `Install` from the `workflow`'s menu. _Reminder, at this stage, you may provide your own values for any of the default `deployment inputs`._


## Uninstallation

Navigate to the deployment and select `Uninstall`. When the uninstall workflow is finished, select `Delete deployment`.
