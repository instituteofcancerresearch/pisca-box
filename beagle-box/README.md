
# Development

### Creating the docker image
You must be in the directory beagle-box/
```
docker build -t beagle-box .
```

### Running locally to test
```
docker run --rm -it beagle-box /bin/bash
```

### Within the command prompt
```
beast -beagle_off -working -overwrite ~/dev/beast-icr/xml/validation.xml

```

### Running the test suit
TODO



### Testing the docker image
```

```

### Pushing the docker image to docker hub
```
docker tag beagle-box rachelicr/beagle-box
docker tag beagle-box rachelicr/beagle-box:vxx

docker push rachelicr/beagle-box
docker push rachelicr/beagle-box:vxx
```

### Running the docker image from docker hub
```
docker pull rachelicr/beagle-box


```

### Running the docker image from singularity hub
```
singularity pull docker://rachelicr/beagle-box



```


### Any problems with singularity on alma, clear out:
```
/home/ralcraft/.local/share/containers/cache
```




