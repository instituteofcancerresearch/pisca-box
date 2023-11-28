# Containerised Wrappers to PISCA and BEAST

This project is intended to create containerised version of pisca to be run easily in HPC/command line environments.  

The goal is to have a docker container for any chosen branch of pisca, in the format dockerfile_branchid.  

Currently there is just dockerfile_master and dockerfile_b1 which will be the first example of a bracnhed container.  

These instructions show how to set up the environment, build the docker image and test/run the docker image.

## For a DEVELOPER

### 1. Running locally to test
```
# test mode allows a check that the directories have been created correctly in the container
python3 app/app.py validate 
# a simple and quick xml file to make sure beast works
python3 app/app.py validation.xml
```

Note, the container may be a more succesful environment than locally to run pisca, so this does not attempt to test the pisca functionality locally.

### 2. Creating the docker image3
Each docker file has the instructions to build and run at the top as each may be a different branch of pisca.

Likewise, each docker image may be pushed to a different place.

### 5. Pushing the docker image to docker hub

To push to docker hub you need an account. The account name goes into the push to docker, eg my account is [rachelicr](https://hub.docker.com/u/rachelicr)
So replace "rachelicr" with your docker usename in the following commands.
And "master" is also the branch being used in this example, so replace with the branch you are using.
The icr has the account icrsc which can add collaborators to repos.

## For a USER

This step can be done independently of all the others, anyone can pull down the docker images and take it from here...

## 6. Running the docker image from docker hub

```
# pull down
docker pull rachelicr/pisca-branch-master
# test/run
docker run rachelicr/pisca-branch-master validate
docker run -v ~/dev/beast-icr/pisca-branch:/mnt --rm rachelicr/pisca-branch-master acna.xml
```

### 7. Running the docker image from singularity hub
```
singularity pull docker://rachelicr/pisca-branch-master
singularity run docker://rachelicr/pisca-branch-master validate
singularity run -B ~/dev/beast-icr/pisca-branch:/mnt docker://rachelicr/pisca-branch-master acna.xml
```

