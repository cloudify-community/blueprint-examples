#!/usr/bin/env bash

ctx logger info "TRYING TO INSTALL IPADDR WE WILL NOT FAIL IF THIS FAILS"
ctx logger info "YOU CAN ALSO RUN sudo yum install -y python-netaddr  on the manager."

RESULT=$(python -c "import ipaddr")

if [[ "${RESULT}" != 0 ]]; then
    if [[ -n "$(command -v yum)" ]]; then
        sudo yum install -y python-netaddr || true
    elif [[ -n "$(command -v apt-get)" ]]; then
        sudo apt-get install -y python-netaddr || true
    fi
fi
