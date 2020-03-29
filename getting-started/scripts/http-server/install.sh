#!/bin/bash -e
cd ~
nohup http-server ~ -p 8080  > /dev/null 2>&1 &
PID=$!
ctx instance runtime_properties pid ${PID}
ctx logger info "PID is ${PID}"

