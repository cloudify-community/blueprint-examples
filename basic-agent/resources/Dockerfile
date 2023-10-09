FROM amd64/centos:7
MAINTAINER Cosmo (hello@cloudify.co)

RUN yum -y update && yum clean all
RUN yum -y install openssh-server  python3 sudo
RUN useradd -m cfyuser
RUN echo "cfyuser ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/cfyuser
RUN chmod 0440 /etc/sudoers.d/cfyuser
RUN mkdir -p /var/log/cloudify
RUN touch /var/log/cloudify/install.log
RUN chmod 0777 /var/log/cloudify/install.log

USER cfyuser
WORKDIR /home/cfyuser

ENV TOKEN={{ TOKEN }}
ENV CM_ENDPOINT={{ CM_ENDPOINT }}
ENV TENANT_NAME={{ TENANT_NAME }}
ENV DEPLOYMENT_ID={{ DEPLOYMENT_ID }}
ENV COMPUTE_NODE_INSTANCE_ID={{ COMPUTE_NODE_INSTANCE_ID }}

COPY ./_copyme.sh /home/cfyuser/download_files.sh

CMD ["/bin/bash", "/home/cfyuser/download_files.sh"]
