#!/bin/bash -e
curl -sL https://rpm.nodesource.com/setup_10.x | sudo -E bash -

sudo setenforce 0
cat << EOF | sudo tee /etc/selinux/config
SELINUX=permissive
SELINUXTYPE=targeted
EOF

sudo yum -y install nodejs
sudo npm install http-server -g
