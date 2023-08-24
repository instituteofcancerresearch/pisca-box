
# Development - pisca-box-vue

### Virtual environment
```
python3 -m venv .venv-vue
source .venv-vue/bin/activate
pip install -r requirements.txt
```

### Running locally to test
```
streamlit run app/app.py
```

### Running the test suit
TODO

### Creating the docker image
You must be in the directory pisca-box/pisca-box-vue/
```
docker build -t pisca-vue .
```

### Testing the docker image
```
docker run --name pisca-vue -p 8000:8501 -v ~/dev/beast-icr/xml:/project/xml pisca-vue
http://localhost:8000/
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







