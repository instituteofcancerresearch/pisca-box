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
