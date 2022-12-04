FROM amd64/centos:7
MAINTAINER Cosmo (hello@cloudify.co)
RUN yum install -y openssh-server openssh-clients
RUN curl "https://bootstrap.pypa.io/pip/2.7/get-pip.py" -o "get-pip.py"
RUN python get-pip.py
RUN pip install --upgrade pip==9.0.1
RUN pip install ansible==2.9.5

WORKDIR /

COPY . create.yaml /
COPY . delete.yaml /
COPY . hosts /