# Containerised Deployment

Due to the complexity of the PISCA environment this project is designed to be deployed in a container.  

## The application container
The develoment container has already been explained. 
The application container uses the development container as a base to minimise time spent building containers and replicating envirnments.

The container image is defined in the `pisca-box-vue/Dockerfile` file.  
It is fairly light and is mostly only an entry point into the copied code installation. 

## Building the application container

This is **NOT FROM INSIDE THE DEVCONTAINER** you want to go back to your local folder (ctrl-sh-p "Reopen in local folder").

If you need to build and deploy the application container (you are probably in the ICR?) use the docker-compose.yml file.  
This has the addition of the listening port, not necessary for manual running of the container, but necessary were it to be deployed on azure.

You can use docker commands, or you can have the docker extenstion installed.  

On the file pisca-box-vue/docker-compose.yml right click and select "Compose Up"  

This will build the image and run it.

## Test the image

You can test the image by running it locally.
```docker run --rm --name pisca-box -p 8002:8501 icrsc/pisca-box```
[localhost:8002](http://localhost:8002) should show the app.

## Push the image to docker hub

You can find the image in the docker dashboard.

Right-click and select push to upload to docker hub (you need access to be able to upload it to github).




