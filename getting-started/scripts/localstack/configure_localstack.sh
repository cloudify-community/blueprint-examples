#!/usr/bin/env bash
# This script is designed to deploy all required prerequisites for localstack docker container.

install_localstack_ubuntu()
{
   echo "this is ubuntu"
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
   sudo apt-get install docker-ce docker-ce-cli containerd.io -y
}


install_localstack_centos()
{
   echo "this is centos"
   sudo yum install -y wget curl \
        apt-transport-https ca-certificates \
        software-properties-common gnupg lsb-release \
        zip unzip pip yum-utils
   # Cleanup previous docker installation if installed
   sudo yum remove docker \
        docker-client \
        docker-client-latest \
        docker-common \
        docker-latest \
        docker-latest-logrotate \
        docker-logrotate \
        docker-engine
   sudo yum-config-manager \
        --add-repo \
        https://download.docker.com/linux/centos/docker-ce.repo
    sudo yum install docker-ce docker-ce-cli containerd.io -y
}


finish_localstack_install ()
{
    sudo systemctl start docker
    if [ $? -ne 0 ]; then
        echo "ERROR: docker service is not started properly!"
        exit 1
    fi
    sudo usermod -a -G docker $USER
    id
    newgrp docker
}


main ()
{
   if [ -f /etc/redhat-release ]; then
      install_localstack_centos
      finish_localstack_install
   else
      install_localstack_ubuntu
      finish_localstack_install
   fi
}


main
