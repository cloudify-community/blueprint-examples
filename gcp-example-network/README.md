
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

  * `gcp_client_x509_cert_url`: A GCP Service Account Client Cert URL.
  * `gcp_client_email`: A GCP Service Account client email.
  * `gcp_client_id`: A GCP Service Account Client ID.
  * `gcp_project_id`: A GCP Project ID.
  * `gcp_private_key_id`: A GCP Project Private Key ID.
  * `gcp_private_key`: A GCP project Private Key. **Hint: Create this secret from a file:** `cfy secrets create private_key -f ./path/to/private-key`.
  * `gcp_region`: A GCP Region such as `us-east1`.
  * `gcp_zone`: A GCP Zone such as `us-east1-b`.
