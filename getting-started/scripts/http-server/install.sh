#!/bin/bash -e
cd /tmp
nohup http-server /tmp -p 8080  > /dev/null 2>&1 &
PID=$!
ctx instance runtime_properties pid ${PID}
ctx logger info "PID is ${PID}"

