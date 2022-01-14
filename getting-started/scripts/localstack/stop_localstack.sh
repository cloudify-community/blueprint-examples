#!/usr/bin/env bash
# Stop command for localstack docker container
# Tested with localstack:0.12.17.5

conainer_name=localstack

# Check docker service
/usr/bin/sudo su - $USER -c "docker ps > /dev/null 2>&1"
if [ $? -eq 0 ]; then
    # Stop container
    container_id=$(docker ps | grep $conainer_name/$conainer_name | awk '{print $1}')
    if [ ! -z $container_id ]; then
       echo "[ $(date +"%m-%d-%Y %H:%M:%S") ] INFO: Stopping $conainer_name $container_id ..."
       /usr/bin/sudo su - $USER -c "docker stop $container_id > /dev/null"
       if [ $? -ne 0 ]; then
          echo "[ $(date +"%m-%d-%Y %H:%M:%S") ] ERROR occured during stopping $conainer_name container!"
          exit 1
       fi
       echo "[ $(date +"%m-%d-%Y %H:%M:%S") ] INFO: Container $conainer_name stopped."
    else
       echo "[ $(date +"%m-%d-%Y %H:%M:%S") ] ERROR: $conainer_name container is not running!"
       exit 1
    fi
else
    echo "[ $(date +"%m-%d-%Y %H:%M:%S") ] ERROR: docker is not running!"
    exit 1
fi
