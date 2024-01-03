# Run the application

Navigate 1 directory in then run the entry point:  
```
cd pisca-box-vue
streamlit run app/home.py
```

The application will pop up in [localhost 8501](http://localhost:8501/)

# Debug the application
https://stackoverflow.com/questions/60172282/how-to-run-debug-a-streamlit-application-from-an-ide
the answer here that starts "If you're a VS Code user,"
In summary, create a launch.json on the debugger (left side) in vscode. 
Add to it this config below, navigate to the app/home.py page and choose to "run".
```
{    
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python:Streamlit",
            "type": "python",
            "request": "launch",
            "module": "streamlit",
            "args": [
                 "run",
                 "${file}",
                 "--server.port",
                 "8501"
            ]
        },
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```
when on the page you want to run, select python:streannlit and press play.






