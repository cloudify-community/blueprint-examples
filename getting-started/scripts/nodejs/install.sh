#!/bin/bash -e
sudo rm -rf /etc/yum.repos.d/google-cloud.repo
sudo yum update -y
curl -fsSL https://rpm.nodesource.com/setup_17.x | sudo bash -

sudo setenforce 0
cat << EOF | sudo tee /etc/selinux/config
SELINUX=permissive
SELINUXTYPE=targeted
EOF

sudo yum -y install nodejs
sudo npm install http-server -g
