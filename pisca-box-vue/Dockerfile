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
# make a dir for the tmp files
RUN mkdir /project/xml

# enable docker inside.... docker!!!!
#https://github.com/jpetazzo/dind
#docker run --privileged -t -i dind

# install docker :shrug: https://docs.docker.com/engine/install/ubuntu/
# Add Docker's official GPG key:
RUN apt-get update -y
RUN apt-get -y install ca-certificates curl gnupg software-properties-common apt-transport-https
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
#echo \
RUN "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update -y

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu `lsb_release -cs` test"
RUN apt update
# To install the latest version, run:
RUN apt-get -y install docker-ce
RUN apt-get -y install docker-ce-cli
RUN apt-get -y install containerd.io
RUN apt-get -y install docker-buildx-plugin
RUN apt-get -y install docker-compose-plugin
    


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
