#!/bin/bash -e

#sudo yum install -y gcc-c++ make curl
#curl -sL https://rpm.nodesource.com/setup_14.x | sudo -E bash -
#sudo yum remove -y nodejs npm
#sudo yum clean all
#sudo yum list available nodejs
# sudo yum install -y nodejs

sudo rm -rf /etc/yum.repos.d/google-cloud.repo
# sudo yum --disablerepo="*" --enablerepo="nodesource" list available

sudo curl -fsSL https://rpm.nodesource.com/setup_14.x | sudo bash -
sudo yum update -y

sudo yum clean all

sudo yum remove node npm nodesource-release-el7-1 -y
sudo yum install epel-release -y
sudo yum install nodejs npm --enablerepo=epel -y

sudo setenforce 0
cat << EOF | sudo tee /etc/selinux/config
SELINUX=permissive
SELINUXTYPE=targeted
EOF

sudo npm install http-server -g
