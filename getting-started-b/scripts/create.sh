#!/bin/bash -e
sudo yum -y install java-1.8.0-openjdk-devel

sudo groupadd -r wildfly
sudo useradd -r -g wildfly -d /opt/wildfly -s /sbin/nologin wildfly

WILDFLY_VERSION=18.0.1.Final

curl -o /tmp/wildfly.tar.gz https://download.jboss.org/wildfly/${WILDFLY_VERSION}/wildfly-${WILDFLY_VERSION}.tar.gz

sudo tar xf /tmp/wildfly.tar.gz -C /opt/
sudo ln -s /opt/wildfly-${WILDFLY_VERSION} /opt/wildfly
sudo chown -RH wildfly: /opt/wildfly

sudo mkdir -p /etc/wildfly
sudo cp /opt/wildfly/docs/contrib/scripts/systemd/wildfly.conf /etc/wildfly/

sudo cp /opt/wildfly/docs/contrib/scripts/systemd/launch.sh /opt/wildfly/bin/
sudo chmod +x /opt/wildfly/bin/*.sh
sudo cp /opt/wildfly/docs/contrib/scripts/systemd/wildfly.service /etc/systemd/system/
sudo /opt/wildfly/bin/add-user.sh -u admin -p admin -e

echo "WILDFLY_CONSOLE_BIND=0.0.0.0" | sudo tee -a /etc/wildfly/wildfly.conf

sudo sed -i 's/$3/$3 -bmanagement $4/' /opt/wildfly/bin/launch.sh
sudo sed -i -r 's/^ExecStart=(.*)$/ExecStart=\1 $WILDFLY_CONSOLE_BIND/' /etc/systemd/system/wildfly.service

sudo mkdir -p /var/run/wildfly/
sudo chown wildfly: /var/run/wildfly/
