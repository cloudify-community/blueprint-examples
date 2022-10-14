#!/bin/bash -e
mkdir -p /tmp/app
cd /tmp/app
nohup http-server /tmp/app -p 8080  > /dev/null 2>&1 &
PID=$!
ctx instance runtime_properties pid ${PID}
ctx logger info "PID is ${PID}"

