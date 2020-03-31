Client Certificate Demo
=======================

Based on https://github.com/sevcsik/client-certificate-demo

The server's private key is in `nodejs/server_*.pem`. This is a self-signed certificate, issued by ourselves (Demo CA).

We have two PEM client certificates
 - `nodejs/alice.pem` which was issued by us (the issuer is Demo CA)
 - `nodejs/bob.pem`, which is a self-signed certificate (the issuer is Bob himself)

Start the server with `cd nodejs && npm install && npm start` in separate console tab.

You can circumvent this by using cURL to call the authenticate endpoint. Note the `--insecure` option: we need this to make cURL accept our Demo CA server certificate.

Check certificates by curl:
```shell
$ curl --insecure --cert nodejs/alice.pem https://localhost:9999/authenticate
Hello Alice, your certificate was issued by Demo CA!
$ curl --insecure --cert nodejs/bob.pem https://localhost:9999/authenticate
Sorry Bob, certificates from Bob are not welcome here.
```

Check certificates by python:
```shell
# no cert
python -c 'import requests; print requests.get("https://localhost:9999/authenticate", verify="nodejs/server_cert.pem").content'

# bob check
python -c 'import requests; print requests.get("https://localhost:9999/authenticate", verify="nodejs/server_cert.pem", cert="bob.pem").content'

# alice check
python -c 'import requests; print requests.get("https://localhost:9999/authenticate", verify="nodejs/server_cert.pem", cert="alice.pem").content'
```

or

```python
import requests

# no certificate
print requests.get("https://localhost:9999/authenticate", verify="nodejs/server_cert.pem").content

# bob
print requests.get("https://localhost:9999/authenticate", verify="nodejs/server_cert.pem", cert="nodejs/bob.pem").content

# alice
print requests.get("https://localhost:9999/authenticate", verify="nodejs/server_cert.pem", cert="nodejs/alice.pem").content
```

Check certificates by blueprint:
```shell
cfy install rest-plugin-cert/client-cert.yaml -i rest-plugin-cert/client-cert-input.yaml
```
