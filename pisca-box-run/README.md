
# Development

### Running locally to test
```
python3 app/app.py validate
python3 app/app.py /home/ralcraft/dev/beast-icr/xml/testStrictClock.xml TEST_MODE # beast test
python3 app/app.py /home/ralcraft/dev/beast-icr/xml/validate.xml TEST_MODE # pisca test
```

### Running locally directly
```
beast -beagle_off -working -overwrite ~/dev/beast-icr/xml/validation.xml
beast -beagle_off -working -overwrite ~/dev/beast-icr/xml/racoon_rabies.xml
beast -beagle_off -overwrite ~/dev/beast-icr/xml/testStrictClock.xml
```

### Running the test suit
TODO

### Creating the docker image
You must be in the directory pisca-box/pisca-box-run/
```
docker build -t pisca-box .
```

### Testing the docker image
```
docker run pisca-box validate
docker run -v ~/dev/beast-icr/xml:/project/xml pisca-box validation.xml
docker run -v ~/dev/beast-icr/xml:/project/xml pisca-box testStrictClock.xml
```

### Pushing the docker image to docker hub
```
docker tag pisca-box rachelicr/pisca-box
docker tag pisca-box rachelicr/pisca-box:v01

docker push rachelicr/pisca-box
docker push rachelicr/pisca-box:v01
```

### Running the docker image from docker hub
```
docker pull rachelicr/pisca-box

docker run rachelicr/pisca-box validate
docker run -v ~/dev/beast-icr/xml:/project/xml rachelicr/pisca-box validation.xml
docker run -v ~/dev/beast-icr/xml:/project/xml rachelicr/pisca-box testStrictClock.xml
```

### Running the docker image from singularity hub
```
singularity pull docker://rachelicr/pisca-box

singularity run docker://rachelicr/pisca-box validate
singularity run -B ~/dev/beast-icr/xml:/project/xml docker://rachelicr/pisca-box validation.xml 
singularity run -B ~/dev/beast-icr/xml:/project/xml docker://rachelicr/pisca-box testStrictClock.xml 
```


### Any problems with singularity on alma, clear out:
```
/home/ralcraft/.local/share/containers/cache
```




