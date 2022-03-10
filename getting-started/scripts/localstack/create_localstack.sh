#!/usr/bin/env bash
# This script is designed to deploy all required prerequisites for localstack docker container.

logfile="/tmp/create_localstack_$(date +'%m-%d-%Y_%H%M%S').log"

install_localstack_ubuntu()
{
   echo "this is ubuntu" | tee -a $logfile
   sudo apt-get update -y 2>/dev/null
   sudo apt-get install -y wget curl apt-transport-https \
        ca-certificates software-properties-common gnupg \
        lsb-release zip unzip pip 2>/dev/null
   # Cleanup previous docker installation if installed
   sudo apt-get remove docker docker-engine docker.io containerd runc
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io -y | tee -a $logfile
}


install_localstack_centos()
{
   echo "this is centos" | tee -a $logfile
   sudo rm -rf /etc/yum.repos.d/google-cloud.repo
   sudo yum update -y
   sudo yum install -y wget curl \
        apt-transport-https ca-certificates \
        software-properties-common gnupg lsb-release \
        zip unzip pip yum-utils | tee -a $logfile
   # Cleanup previous docker installation if installed
   sudo yum remove docker \
        docker-client \
        docker-client-latest \
        docker-common \
        docker-latest \
        docker-latest-logrotate \
        docker-logrotate \
        docker-engine | tee -a $logfile
   sudo yum install -y yum-utils
   sudo yum-config-manager \
        --add-repo \
        https://download.docker.com/linux/centos/docker-ce.repo
    sudo yum install docker-ce docker-ce-cli containerd.io -y | tee -a $logfile
}


finish_localstack_install ()
{
    echo "INFO: Starting finish_localstack_install function" | tee -a $logfile
    sudo systemctl start docker | tee -a $logfile
    if [ $? -ne 0 ]; then
        echo "ERROR: docker service is not started properly!"| tee -a $logfile
        exit 1
    fi
    sudo usermod -a -G docker $USER | tee -a $logfile
    id | tee -a $logfile
#    nohup newgrp docker &  # | tee -a $logfile
    echo "INFO: Finishing finish_localstack_install function" | tee -a $logfile
}


main ()
{
   if [ -f /etc/redhat-release ]; then
      install_localstack_centos
      finish_localstack_install
      exit 0
   else
      install_localstack_ubuntu
      finish_localstack_install
      exit 0
   fi
}


main
