#!/bin/bash -e

sudo yum install -y gcc-c++ make curl
curl -sL https://rpm.nodesource.com/setup_14.x | sudo -E bash -
sudo yum remove -y nodejs npm
sudo yum clean all
sudo yum list available nodejs
sudo yum install -y nodejs

sudo rm -rf /etc/yum.repos.d/google-cloud.repo
# sudo yum --disablerepo="*" --enablerepo="nodesource" list available

sudo yum update -y
curl -fsSL https://rpm.nodesource.com/setup_17.x | sudo bash -

sudo setenforce 0
cat << EOF | sudo tee /etc/selinux/config
SELINUX=permissive
SELINUXTYPE=targeted
EOF

sudo npm install http-server -g
