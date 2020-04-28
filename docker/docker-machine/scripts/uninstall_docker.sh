#!/bin/bash -e

if [ -f /etc/redhat-release ]; then
  yum remove -y docker
fi

if [ -f /etc/lsb-release ]; then
  apt-get remove -y docker
fi
