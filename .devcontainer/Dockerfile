################### BUILD AND RUN THIS DOCKER FILE ############################

### BUILD IMAGE

# docker build -t rachelicr/pisca-1-dev -f .devcontainer/Dockerfile .


### TEST IMAGE

# docker push rachelicr/pisca-1-dev

#################################################################################
# Image downloaded with advice from: # https://stackoverflow.com/questions/54437030/how-can-i-create-a-docker-image-to-run-both-python-and-r
FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends build-essential r-base r-cran-randomforest python3.10 python3-pip python3-setuptools python3-dev
WORKDIR /app
ADD requirements.txt .
ADD requirements.r .
# installing python libraries
RUN pip3 install -r requirements.txt
# installing r libraries
RUN Rscript requirements.r
COPY . /app
#######################################################################################
# The pisca special additions needed
WORKDIR /project
COPY . /project
# Install software 
RUN apt-get update -y
RUN apt-get install -y openssh-client
RUN apt-get install -y wget
ENV JAVA_HOME=/project/jdk-20.0.2
ENV PATH=$JAVA_HOME/bin:$PATH
ENV PATH=/project/BEASTv1.8.4/bin:$PATH
# install the correct version of java!!!!!
#RUN wget -O jdk.tar.gz https://download.oracle.com/java/20/latest/jdk-20_linux-x64_bin.tar.gz
# it looks like that version has been moved to the archive between 10/10/23 and 17/10/23
RUN wget -O jdk.tar.gz https://download.oracle.com/java/20/archive/jdk-20.0.2_linux-x64_bin.tar.gz
RUN tar zxvf jdk.tar.gz
## makes directory jdk-20.0.2
# Install beast
RUN wget -O beast.tgz https://github.com/beast-dev/beast-mcmc/releases/download/v1.8.4/BEASTv1.8.4.tgz
RUN tar -xvzf beast.tgz
## makes directory BEASTv1.8.4
# Install pisca
RUN wget -O pisca.tgz https://github.com/adamallo/PISCA/releases/download/v1.1/PISCAv1.1.tgz
RUN tar -xvzf pisca.tgz
## makes directory PISCAv1.1 ## note that cd has to be inline with other commands
RUN chmod +x /project/PISCAv1.1/install.sh
RUN cd /project/PISCAv1.1/ && ./install.sh /project/BEASTv1.8.4/
# make a dir for the tmp files
RUN mkdir /project/xml
