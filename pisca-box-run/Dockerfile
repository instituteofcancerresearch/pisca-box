# install operating sustem and java 
FROM python:3.12-rc
#FROM ubuntu:22.04
# FROM python:3.11-slim-bookworm
WORKDIR /project
COPY . /project

# Install software 
RUN apt-get update -y
##RUN apt-get install -y git
RUN apt-get install -y openssh-client
RUN apt-get install -y wget

ENV JAVA_HOME=/project/jdk-20.0.2
ENV PATH=$JAVA_HOME/bin:$PATH


# install the correct version of java!!!!!
#RUN apt-get install -y default-jdk
RUN wget -O jdk.tar.gz https://download.oracle.com/java/20/latest/jdk-20_linux-x64_bin.tar.gz
RUN tar zxvf jdk.tar.gz
#RUN export JAVA_HOME=/project/jdk-20.0.2
#RUN export PATH=$JAVA_HOME/bin:$PATH
#COPY /project/jdk-20.0.2/bin /usr/bin
#RUN apt install -f
#RUN update-alternatives --install /usr/bin/java java /project/jdk-20.0.2/bin/java 1
#RUN update-alternatives --install /usr/bin/javac javac /project/jdk-20.0.2/bin/javac 1

#RUN wget -O jdk.deb https://download.oracle.com/java/20/latest/jdk-20_linux-x64_bin.deb
#RUN yes | apt install /project/jdk.deb

#RUN wget -O jdk.rpm https://download.oracle.com/java/20/latest/jdk-20_linux-x64_bin.rpm
#RUN yes | apt-get install alien
#RUN alien -i jdk.rpm
##RUN dpkg -i jdk.deb



# Install beast
RUN wget -O beast.tgz https://github.com/beast-dev/beast-mcmc/releases/download/v1.8.4/BEASTv1.8.4.tgz
RUN tar -xvzf beast.tgz
## makes directory BEASTv1.8.4

# Install pisca
## - not used now RUN git clone https://github.com/adamallo/PISCA.git
RUN wget -O pisca.tgz https://github.com/adamallo/PISCA/releases/download/v1.1/PISCAv1.1.tgz
RUN tar -xvzf pisca.tgz
## makes directory PISCAv1.1 - ## note that cd has to be inline with other commands
RUN chmod +x /project/PISCAv1.1/install.sh
RUN cd /project/PISCAv1.1/ && ./install.sh /project/BEASTv1.8.4/

# make a dir for the tmp files
RUN mkdir /project/tmp

####### Commands to run python application #######################
ENTRYPOINT ["python3", "app/app.py"]
# OR Either stop here to look in the container with BASH
#CMD tail -f /dev/null
##################################################################

# Running as a cmd app
# docker run --rm -it pisca-box-run /bin/bash
# /project/BEASTv1.8.4/bin/beast -beagle_off -working -overwrite /project/BEASTv1.8.4/examples/testXML/testLikelihood.xml

## Running the docker app
# docker build -t pisca-box-run .
# docker run -v ~/dev/beast-icr/xml:/project/tmp pisca-box-run validate
# docker run -v ~/dev/beast-icr/xml:/project/tmp pisca-box-run pisca01
# docker run -v ~/dev/beast-icr/xml:/project/tmp pisca-box-run beast01 racoon_rabies.xml
# docker run -v ~/dev/beast-icr/xml:/project/tmp pisca-box-run beast01 testStrictClock.xml
## PISCA
# docker run -v ~/dev/beast-icr/xml:/project/tmp pisca-box-run beast01 validation.xml

## Running locally directly
# beast -beagle_off -working -overwrite ~/dev/beast-icr/xml/validation.xml
# beast -beagle_off -working -overwrite ~/dev/beast-icr/xml/racoon_rabies.xml
# beast -beagle_off -overwrite ~/dev/beast-icr/xml/testStrictClock.xml

## running from python, locally
# python3 app/app.py beast01 racoon_rabies.xml


