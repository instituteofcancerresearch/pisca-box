FROM python:3.11-slim-bookworm

# install operating sustem and java 
# FROM ubuntu:18.04
# FROM python:3.11-slim-bookworm
WORKDIR /project
COPY . /project

# Install software 
RUN apt-get update -y
#RUN apt-get install -y git
RUN apt-get install -y openssh-client
RUN apt-get install -y wget
RUN apt-get install -y default-jdk

# Install beast
RUN wget -O beast.tgz https://github.com/beast-dev/beast-mcmc/releases/download/v1.8.4/BEASTv1.8.4.tgz
RUN tar -xvzf beast.tgz
## makes directory BEASTv1.8.4

# Install pisca
#RUN git clone https://github.com/adamallo/PISCA.git
#RUN wget -O pisca.tgz https://github.com/adamallo/PISCA/releases/download/v1.1/PISCAv1.1.tgz
#RUN tar -xvzf pisca.tgz
## makes directory PISCAv1.1
#RUN chmod +x /project/PISCAv1.1/install.sh
#RUN cd /project/PISCAv1.1/ && ./install.sh /project/BEASTv1.8.4/
## note that cd has to be inline with other commands

# make a dir for the tmp files
RUN mkdir /project/tmp
# Commands to run python application
ENTRYPOINT ["python3", "app/app.py"]
# OR Either stop here to look in the container with BASH
#CMD tail -f /dev/null

# Running as a cmd app
# docker run --rm -it pisca-box-run /bin/bash
# /project/BEASTv1.8.4/bin/beast -beagle_off -working -overwrite /project/BEASTv1.8.4/examples/testXML/testLikelihood.xml

## Running the docker app
# docker build -t pisca-box-run .
# docker run -v ~/dev/beast-icr/xml:/project/tmp pisca-box-run validate
# docker run -v ~/dev/beast-icr/xml:/project/tmp pisca-box-run pisca01
# docker run -v ~/dev/beast-icr/xml:/project/tmp pisca-box-run beast01 racoon_rabies.xml
# docker run -v ~/dev/beast-icr/xml:/project/tmp pisca-box-run beast01 testStrictClock.xml

## Running locally directly
# beast -beagle_off -working -overwrite ~/dev/beast-icr/xml/validation.xml
# beast -beagle_off -working -overwrite ~/dev/beast-icr/xml/racoon_rabies.xml
# beast -beagle_off -overwrite ~/dev/beast-icr/xml/testStrictClock.xml


