# Containerised Development

Due to the complexity of the PISCA environment this project is designed to be developed and debugged in a container.  

Thus, VSCode is the IDE of choice, as the ability use conatiners for development is integrated and free. It is also possible in a paid-foir version of pycharm.  
You will need the Dev Containers extension installed.

## The container
The develoment container is defined in the `devcontainer.json` file. This file defines the container image to be used, the extensions to be installed and the settings to be used.

The container image is defined in the `Dockerfile` file. This file defines the base image to be used and the additional packages to be installed.

## Building the container
- You should not need to build the container, it can pull down from docker automatically
- Should you need to, the instructions for building are at the top of the Dockerfile

## Using the container
- ctrl-sh-p in vscode and select "Devcontainers: Repoen in container"

You will see the file system much as before, this time in Workspaces/pisca-box a pseudo linux operating system.  
It will feel a bit different to an ordinary dev environment as for example there is no virtual environment, that was all installed in the container.  

If you find a need to add a python library or R library they need to go in the container and then it needs to be rebuilt and redistributed.

Check it is as you would expect:  
```R --version``` will give 4.3.2  
```beast``` will throw java errors - but it is there  

## Installations from the marketplace
You will not have pulled in any of your markletplace extensions so they need re-installing: warning every time the container is rebuilt they need to be re-installed so don't get too comfortable.






