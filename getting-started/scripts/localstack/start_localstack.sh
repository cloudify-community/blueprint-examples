#!/usr/bin/env bash
# Startup command for localstack docker container
# Tested with localstack:0.12.17.5

lsver=0.12.17.5
logfile="/tmp/start_localstack_$(date +'%m-%d-%Y_%H%M%S').log"
conainer_name=localstack

# Check docker service
/usr/bin/sudo su - $USER -c "docker ps > /dev/null 2>&1"
if [ $? -eq 0 ]; then
    container_id=$(docker ps | grep $conainer_name/$conainer_name | awk '{print $1}')
    if [ ! -z $container_id ]; then
        echo "[ $(date +"%m-%d-%Y %H:%M:%S") ] ERROR: Container $conainer_name is already running!" | tee -a $logfile
        exit 1
    fi
    # Start container
    echo "[ $(date +"%m-%d-%Y %H:%M:%S") ] INFO: Starting container ..." | tee -a $logfile
    /usr/bin/sudo su - $USER -c "docker run --rm -d -p 4566:4566 -p 4571:4571 localstack/localstack:$lsver" | tee -a $logfile
    exit 0
else
    echo "[ $(date +"%m-%d-%Y %H:%M:%S") ] ERROR: docker is not running!" | tee -a $logfile
    exit 1
fi
