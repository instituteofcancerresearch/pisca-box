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
FROM rachelicr/env-pisca-v1 as base
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
#RUN mkdir /project/xml
EXPOSE 8501
COPY . .
####### Commands to run python application #######################
ENTRYPOINT [ "streamlit", "run" ]
CMD [ "/project/app/home.py", "--server.headless", "true", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"]

