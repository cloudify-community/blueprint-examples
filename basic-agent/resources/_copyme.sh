#!/bin/bash

sudo mkdir -p /opt/cloudify-agent/agent-7.0.0
sudo mkdir -p /opt/cloudify-agent-7.0.0/${COMPUTE_NODE_INSTANCE_ID}/cloudify/ssl
sudo mkdir -p /var/log/cloudify/
sudo touch /var/log/cloudify/agent-install.log
sudo touch /var/log/cloudify/agent.log
sudo chown cfyuser:cfyuser -R /var/log/cloudify
sudo chown cfyuser:cfyuser -R /opt/cloudify-agent-7.0.0

curl -X GET --header "Tenant: ${TENANT_NAME}" --header "Authentication-Token: ${TOKEN}" --insecure https://${CM_ENDPOINT}:443/resources/packages/agents/manylinux-x86_64-agent.tar.gz -o /tmp/manylinux-x86_64-agent.tar.gz

until RESULT=`curl --silent -X GET --header "Tenant: ${TENANT_NAME}" --header "Authentication-Token: ${TOKEN}" --insecure "https://${CM_ENDPOINT}:443//api/v3.1/node-instances/${COMPUTE_NODE_INSTANCE_ID}?_include=runtime_properties" | python -c "import sys, json; print json.load(sys.stdin)[\"runtime_properties\"][\"cloudify_agent\"][\"install_script_download_link\"]"`;
do
  echo "..."
  sleep 1
done

curl -X GET --header "Tenant: ${TENANT_NAME}" --header "Authentication-Token: ${TOKEN}" --insecure https://${CM_ENDPOINT}:443/resources/deployments/default_tenant/${DEPLOYMENT_ID}/${RESULT} -o /tmp/create-cfy-agent-script.sh

sed -i "/AGENT_DIR=/c\AGENT_DIR=\"/opt/cloudify-agent/agent-7.0.0\"" /tmp/create-cfy-agent-script.sh
sed -i "/AGENT_USER=/c\AGENT_USER=\"cfyuser\"" /tmp/create-cfy-agent-script.sh

sudo tar xzvf /tmp/manylinux-x86_64-agent.tar.gz --strip=1 -C /opt/cloudify-agent/agent-7.0.0/

# sudo /opt/cloudify-agent/agent-7.0.0/env/bin/cfy-agent/env/bin/cfy-agent" configure --fix-shebangs
sudo mkdir -p /home/jenkins/agent/workspace/Build-Agents/x86_64/cloudify/
sudo ln -s /opt/cloudify-agent/agent-7.0.0/env/  /home/jenkins/agent/workspace/Build-Agents/x86_64/cloudify/env
sudo chown cfyuser:cfyuser -R /home/jenkins

sudo chmod 700 /tmp/create-cfy-agent-script.sh
sudo chown cfyuser:cfyuser /tmp/create-cfy-agent-script.sh
/bin/bash /tmp/create-cfy-agent-script.sh >> /var/log/cloudify/install.log

/home/jenkins/agent/workspace/Build-Agents/x86_64/cloudify/env/bin/python -m cloudify_agent.worker --queue "${COMPUTE_NODE_INSTANCE_ID}" --max-workers 5 --name "${COMPUTE_NODE_INSTANCE_ID}" >&1 | tee /var/log/cloudify/agent.log
