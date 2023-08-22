# install operating sustem and java 
# FROM ubuntu:18.04
# FROM python:3.11-slim-bookworm
WORKDIR /project
COPY . /project

# Install software 
RUN apt-get update -y
RUN apt-get install -y git
RUN apt-get -y install openssh-client
RUN apt-get install -y wget
RUN apt-get install -y default-jdk

# Install beast
RUN wget -O beast.tgz https://github.com/beast-dev/beast-mcmc/releases/download/v1.8.4/BEASTv1.8.4.tgz
RUN tar -xvzf beast.tgz
## makes directory BEASTv1.8.4

# Install pisca
#RUN git clone https://github.com/adamallo/PISCA.git
RUN wget -O pisca.tgz https://github.com/adamallo/PISCA/releases/download/v1.1/PISCAv1.1.tgz
RUN tar -xvzf pisca.tgz
## makes directory PISCAv1.1
RUN chmod +x /project/PISCAv1.1/install.sh
RUN cd /project/PISCAv1.1/ && ./install.sh /project/BEASTv1.8.4/
## note that cd has to be inline with other commands
