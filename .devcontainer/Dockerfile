################### BUILD AND RUN THIS DOCKER FILE ############################

### BUILD IMAGE
# docker build -t rachelicr/env-pisca-v1 -f .devcontainer/Dockerfile .

### USE IMAGE
# ctrl-sh-p in vscode and select the image

### TAG IMAGE
# docker tag rachelicr/env-pisca-v1 rachelicr/env-pisca-v1:v07

### PUSH IMAGE
# docker push rachelicr/env-pisca-v1:v01
# docker push rachelicr/env-pisca-v1

#################################################################################
# Image downloaded with advice from: # https://stackoverflow.com/questions/54437030/how-can-i-create-a-docker-image-to-run-both-python-and-r
###########################################################################
###################### THEN INSTALL PYTHON ################################
###########################################################################
FROM ubuntu:latest
#FROM r-base:4.3.2
COPY . /app
ENV DEBIAN_FRONTEND=noninteractive
#RUN apt-get update && apt-get install -y --no-install-recommends build-essential r-base r-cran-randomforest python3.10 python3-pip python3-setuptools python3-dev
RUN apt-get update && apt-get install -y --no-install-recommends build-essential python3.10 python3-pip python3-setuptools python3-dev
###########################################################################
############# # installing python libraries  ##############################
###########################################################################
ADD requirements.txt .
ADD requirements.R .
RUN pip3 install -r requirements.txt
###########################################################################
WORKDIR /project
COPY . /project
# Install software 
RUN apt-get update -y
RUN apt-get install -y openssh-client
RUN apt-get install -y wget
###########################################################################
###################### INSTALL R ################################
###########################################################################
RUN apt-get install -y gdebi-core
RUN wget -O r-4.3.2_1_amd64.deb https://cdn.rstudio.com/r/ubuntu-2204/pkgs/r-4.3.2_1_amd64.deb
RUN gdebi -n r-4.3.2_1_amd64.deb
ENV PATH=/opt/R/4.3.2/bin:$PATH
# install required R libraries
RUN R -e "install.packages('ape',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('jsonlite',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('data.table',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('ggplot2',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('cowplot',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('HDInterval',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('lubridate',dependencies=TRUE, repos='http://cran.rstudio.com/')"
# And from BIOCMANAGER
RUN R -e "install.packages('BiocManager',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "BiocManager::install('treeio')"
RUN R -e "BiocManager::install('ggtree')"
###########################################################################
###################### THEN INSTALL BEAST/PISCA ###########################
###########################################################################
RUN apt-get update -y
ENV JAVA_HOME=/project/jdk-20.0.2
ENV PATH=$JAVA_HOME/bin:$PATH
ENV PATH=/project/BEASTv1.8.4/bin:$PATH
# install the correct version of java!!!!!  - makes directory jdk-20.0.2
RUN wget -O jdk.tar.gz https://download.oracle.com/java/20/archive/jdk-20.0.2_linux-x64_bin.tar.gz
RUN tar zxvf jdk.tar.gz
# Install beast - makes directory BEASTv1.8.4
RUN wget -O beast.tgz https://github.com/beast-dev/beast-mcmc/releases/download/v1.8.4/BEASTv1.8.4.tgz
RUN tar -xvzf beast.tgz
# Install pisca - ## makes directory PISCAv1.1 ## note that cd has to be inline with other commands
RUN wget -O pisca.tgz https://github.com/adamallo/PISCA/releases/download/v1.1/PISCAv1.1.tgz
RUN tar -xvzf pisca.tgz
RUN chmod +x /project/PISCAv1.1/install.sh
RUN cd /project/PISCAv1.1/ && ./install.sh /project/BEASTv1.8.4/
# make a dir for the tmp files
RUN mkdir /project/xml


