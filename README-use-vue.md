# Pisca-Box: A containerisation of PISCA

## Summary
Pisca-Box consists of 2 containerised applications to run PISCA.

pisca-box is the command line interface that gives identical functionality and inputs as PISCA, but being containersied is operating system independent and through singularity can be run on the command line from alma.

pisca-vue is a locally hosted streamlit application to give a user-friendly interface for xml generation, help and instructions. Also containerised this is intended to provide both a way to generate xml and also form a platform for creating tutorials and help.

## Pull from docker
```
docker pull rachelicr/pisca-vue
docker run --rm --name pisca-vue -p 8002:8501 rachelicr/pisca-vue
```
The --rm removes the docker container on exit so you don't need to manually remove it. 
If you want to re-use the container you can create it once and then run it when you want:
```
docker create --name pisca-vue-dock -p 8002:8501 rachelicr/pisca-vue
docker start pisca-vue-dock
```
The application is locally hosted, so is available on the port you specify, in this case 8002:
[localhost](http://localhost:8002/)



