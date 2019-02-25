#!/bin/bash

ctx logger info "Creating fauxapi-auth token"
fauxapi_apikey=${api_key}
fauxapi_apisecret=${api_secret}

fauxapi_timestamp=`date -u +%Y%m%dZ%H%M%S`
fauxapi_nonce=`head -c 40 /dev/urandom | (md5sum 2>/dev/null  || md5 2>/dev/null) | head -c 8`

# NB:-
#  auth = apikey:timestamp:nonce:HASH(apisecret:timestamp:nonce)

fauxapi_hash=`echo -n ${fauxapi_apisecret}${fauxapi_timestamp}${fauxapi_nonce} | (sha256sum 2>/dev/null  || shasum -a 256 2>/dev/null) | cut -d' ' -f1`
fauxapi_auth=${fauxapi_apikey}:${fauxapi_timestamp}:${fauxapi_nonce}:${fauxapi_hash}

ctx instance runtime_properties 'fauxapi_auth' ${fauxapi_auth}
ctx logger info "Successfully created fauxapi-auth token"
