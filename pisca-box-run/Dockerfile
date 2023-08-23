# install operating sustem and java 
FROM python:3.12-rc-slim-bookworm
#FROM python:3.12-rc

WORKDIR /project
COPY . /project

# Install software 
RUN apt-get update -y
RUN apt-get install -y openssh-client
RUN apt-get install -y wget

ENV JAVA_HOME=/project/jdk-20.0.2
ENV PATH=$JAVA_HOME/bin:$PATH

# install the correct version of java!!!!!
RUN wget -O jdk.tar.gz https://download.oracle.com/java/20/latest/jdk-20_linux-x64_bin.tar.gz
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

####### Commands to run python application #######################
ENTRYPOINT ["python3", "app/app.py"]
# OR stop here to look in the container with BASH
#CMD tail -f /dev/null

################################################################
## Commands to run the docker container
# Running as a cmd app
# docker run --rm -it pisca-box-run /bin/bash
# /project/BEASTv1.8.4/bin/beast -beagle_off -working -overwrite /project/BEASTv1.8.4/examples/testXML/testLikelihood.xml
################################################################
############ Updating to docker ################################
# docker tag pisca-box-run rachelicr/pisca-box-run
# docker push rachelicr/pisca-box-run

################ Running the docker app ########################
# docker build -t pisca-box-run .
# docker run -v ~/dev/beast-icr/xml:/project/xml pisca-box-run validate
# docker run -v ~/dev/beast-icr/xml:/project/xml pisca-box-run pisca01
# docker run -v ~/dev/beast-icr/xml:/project/xml pisca-box-run beast01 testStrictClock.xml
## PISCA
# docker run -v ~/dev/beast-icr/xml:/project/xml pisca-box-run beast01 validation.xml

################## Running locally directly #####################
# beast -beagle_off -working -overwrite ~/dev/beast-icr/xml/validation.xml
# beast -beagle_off -working -overwrite ~/dev/beast-icr/xml/racoon_rabies.xml
# beast -beagle_off -overwrite ~/dev/beast-icr/xml/testStrictClock.xml

################## running from python, locally #################
# python3 app/app.py beast01 racoon_rabies.xml

################################################################

## Running it with singularity from docker hub
# singularity pull docker://rachelicr/pisca-box-run
# singularity run docker://rachelicr/pisca-box-run validate

# singularity run -B ~/dev/beast-icr/xml:/project/xml docker://rachelicr/pisca-box-run files
# singularity run -B ~/dev/beast-icr/xml:/project/xml docker://rachelicr/pisca-box-run beast01 validation.xml 
# singularity run -B ~/dev/beast-icr/xml:/project/xml docker://rachelicr/pisca-box-run beast01 testStrictClock.xml 

## Running it with singularity from docker hub
# docker pull rachelicr/pisca-box-run
# docker run -v ~/dev/beast-icr/xml:/project/xml rachelicr/pisca-box-run files
# docker run -v ~/dev/beast-icr/xml:/project/xml rachelicr/pisca-box-run beast01 testStrictClock.xml
# docker run -v ~/dev/beast-icr/xml:/project/xml rachelicr/pisca-box-run beast01 validation.xml

