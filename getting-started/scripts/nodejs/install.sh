#!/bin/bash -e
curl -fsSL https://rpm.nodesource.com/setup_current.x | sudo bash -

sudo setenforce 0
cat << EOF | sudo tee /etc/selinux/config
SELINUX=permissive
SELINUXTYPE=targeted
EOF

sudo yum -y install nodejs
sudo npm install http-server -g
