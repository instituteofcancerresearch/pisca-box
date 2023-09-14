
# Development - pisca-box-vue

### Virtual environment
```
python3 -m venv .venv-vue
source .venv-vue/bin/activate
pip install -r requirements.txt -U
```

### Running locally to test
```
streamlit run app/home.py
```
It is then available (usually) on http://localhost:8501/

### Running the test suit
TODO

### Creating the docker image
You must be in the directory pisca-box/pisca-box-vue/
```
docker build -t pisca-vue .
```

### Testing the docker image
```
docker run --rm --name pisca-vue-dev -p 8002:8501 pisca-vue
http://localhost:8002/
```

### Pushing the docker image to docker hub
```
docker tag pisca-vue rachelicr/pisca-vue
docker tag pisca-vue rachelicr/pisca-vue:v06

docker push rachelicr/pisca-vue
docker push rachelicr/pisca-vue:v06
```

### Running the docker image from docker hub
```
docker pull rachelicr/pisca-vue
docker run --name pisca-vue -p 8001:8501 rachelicr/pisca-vue
docker start pisca-vue
```


### debug and run in vscode
https://stackoverflow.com/questions/60172282/how-to-run-debug-a-streamlit-application-from-an-ide
the answer here that starts "If you're a VS Code user,"
In summary, create a launch.json on the debugger (left side) in vscode. Add to it this config:
```
{
    "name": "Python:Streamlit",
    "type": "python",
    "request": "launch",
    "module": "streamlit",
    "args": [
         "run",
         "${file}",
         "--server.port",
         "SPECIFY_YOUR_OWN_PORT_NUMBER_HERE"
    ]
}
```
when on the page you want to run, select python:streannlit and press play.






