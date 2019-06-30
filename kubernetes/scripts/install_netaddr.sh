#!/usr/bin/env bash

RESULT=$(python -c "import ipaddr")

if [[ "${RESULT}" != 0 ]]; then
    if [[ -n "$(command -v yum)" ]]; then
        sudo yum install -y python-netaddr
    elif [[ -n "$(command -v apt-get)" ]]; then
        sudo apt-get install -y python-netaddr
    fi
    /opt/mgmtworker/env/bin/pip install netaddr
fi
