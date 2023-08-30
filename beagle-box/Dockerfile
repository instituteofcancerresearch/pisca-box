
# install operating sustem and java 

######################################################################
### either ###
######################################################################
#https://forums.developer.nvidia.com/t/unable-to-locate-package-cuda-command-line-tools-10-2-with-apt-get-when-building-docker-image-for-jetpack-4-6/187839
ARG CUDA=10.2
FROM nvcr.io/nvidia/l4t-cuda:10.2.460-runtime
ARG CUDA
RUN apt-get update -y
RUN apt-get install -y cuda
######################################################################
### or ###
######################################################################
#FROM python:3.12-rc-slim-bookworm
######################################################################

WORKDIR /project
COPY . /project

# Install software 
RUN apt-get update -y
RUN apt-get install -y openssh-client wget git software-properties-common cmake build-essential autoconf automake libtool pkg-config 
RUN apt-get update -y
RUN apt-get install -y  cuda
RUN apt-get update -y


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

## INSTALL CUDA GPU SUPPORT
# https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Debian&target_version=10&target_type=deb_network
RUN apt-get update -y
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/debian10/x86_64/cuda-keyring_1.1-1_all.deb
RUN dpkg -i cuda-keyring_1.1-1_all.deb
RUN add-apt-repository contrib
#RUN apt-get install -y cuda
#RUN apt-get update -y
## INSTALL BEAGLE
#RUN apt-get install cmake build-essential autoconf automake libtool git pkg-config openjdk-11-jdk

RUN apt-get update -y
RUN git clone --depth=1 https://github.com/beagle-dev/beagle-lib.git
RUN cd beagle-lib
RUN mkdir build
RUN cd build && cmake -DCMAKE_INSTALL_PREFIX:PATH=$HOME .. && make install

# make a dir for the tmp files
#RUN mkdir /project/xml
#RUN mkdir /mnt

####### Commands to run python application #######################
#ENTRYPOINT ["python3", "/project/app/app.py"]
#CMD ["python3", "/app/app.py"]
# OR stop here to look in the container with BASH
CMD tail -f /dev/null

################################################################
## Commands to run the docker container
# docker build -t pisca-box .
# Running as a cmd app
# docker run --rm -it pisca-box /bin/bash
################################################################
