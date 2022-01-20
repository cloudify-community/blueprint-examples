#!/usr/bin/env bash
# Installation of aws cli and awslocal cli to interact with localstack.

install_cli_ubuntu()
{
   echo "this is ubuntu"
   sudo apt install python3-pip unzip -y
}


install_cli_centos()
{
   echo "this is centos"
   sudo yum install python3-pip unzip -y
}

finish_cli_install ()
{
   awsclizip="https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
   pip3 install awscli-local --user
   curl ${awsclizip} -o "awscliv2.zip"
   if [ $? -ne 0 ]; then
      echo "ERROR: download of ${awsclizip} is failed!"
   fi
   unzip awscliv2.zip > /dev/null 2>&1
   if [ $? -ne 0 ]; then
      echo "ERROR: unzip command returned exit code $?!"
      exit 1
   fi
   sudo ./aws/install
   PATH=$PATH:/home/${USER}/.local/bin
}

main ()
{
   if [ -f /etc/redhat-release ]; then
      install_cli_centos
      finish_cli_install
   else
     install_cli_ubuntu
     finish_cli_install
   fi
}


main
