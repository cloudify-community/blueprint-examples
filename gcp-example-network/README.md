
# GCP Example Network

### Resources Created

  * `network`
  * `subnet`


## Compatibility

Tested with:
  * Cloudify 4.5.5


## Pre-installation steps

Upload the required plugins:

  * [GCP Plugin](https://github.com/cloudify-cosmo/cloudify-gcp-plugin/releases).


If you do not provide your own `deployment inputs` below, you must add these secrets to your Cloudify Manager `tenant`:

  * `gcp_credentials`: A GCP service account key in JSON format. **Hint: Create this secret from a file:** `cfy secrets create gcp_credentials -f ./path/to/JSON key`.

