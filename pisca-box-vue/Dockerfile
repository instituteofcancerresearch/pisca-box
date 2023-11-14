################### BUILD AND RUN THIS DOCKER FILE ############################

### BUILD IMAGE

# docker build -t pisca-box-vue .

### TEST IMAGE

# docker run --rm --name pisca-box-vue -p 8002:8501 pisca-box-vue
# runs on http://localhost:8002/

### UPLOAD TO DOCKER

# docker tag pisca-box-vue rachelicr/pisca-box-vue
# docker push rachelicr/pisca-box-vue

### Pull DOWN FROM DOCKER and run

# docker pull rachelicr/pisca-box-vue

### TEST IMAGE

# docker run --rm --name p-b-v -p 8003:8501 rachelicr/pisca-box-vue
# runs on http://localhost:8003/


#################################################################################

# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1
# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

#############################################################
WORKDIR /project
COPY . /project
# Install software 
RUN apt-get update -y
RUN apt-get install -y openssh-client
RUN apt-get install -y wget
##################################################################################################
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
###################################################################################################
# make a dir for the tmp files
RUN mkdir /project/xml


# enable docker inside.... docker!!!!
#RUN apt-get update -y
#RUN apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
#RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
#RUN apt-key fingerprint 0EBFCD88
#RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
#RUN apt-get update -y
#RUN apt-get install -y docker-ce docker-ce-cli containerd.io
#RUN docker run hello-world




# install R packages
#https://support.bioconductor.org/p/p134101/
#https://stackoverflow.com/questions/45244387/install-r-in-docker-image
#RUN apt-get update -y 
#RUN apt-get install -y r-base
# Docker inheritance
#FROM bioconductor/bioconductor_docker:devel as dev
#RUN R -e 'install.packages("BiocManager")'
#RUN R -e "BiocManager::install(version='devel')"
#RUN R -e 'BiocManager::install(c("treeio","ggtree", "HDInterval", "lubridate", ask = F))'
# install renv & restore packages
#RUN R -e "install.packages('data.table',dependencies=TRUE, repos='http://cran.rstudio.com/')"
#RUN R -e "install.packages('ggplot2',dependencies=TRUE, repos='http://cran.rstudio.com/')"
#RUN R -e "install.packages('cowplot',dependencies=TRUE, repos='http://cran.rstudio.com/')" 

# install python packages
RUN apt-get update -y
RUN python -m pip install -r requirements.txt

EXPOSE 8501
COPY . .
####### Commands to run python application #######################
#CMD streamlit run app/app.py
ENTRYPOINT [ "streamlit", "run" ]
CMD [ "/project/app/home.py", "--server.headless", "true", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"]
# OR stop here to look in the container with BASH
#CMD tail -f /dev/null
