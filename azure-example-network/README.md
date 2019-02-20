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
