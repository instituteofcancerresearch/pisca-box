import streamlit as st
import os
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import StringIO
import subprocess

@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret
        
        stdout.write = new_write
        yield
    
def run_validation(dirs):
    """Run validation command."""    
    print("listing files...")
    result = subprocess.run(["ls","-l"],stdout=subprocess.PIPE)    
    if result:
        print(result.stdout.decode('utf-8'))    
    for dir in dirs:
        result = subprocess.run(["ls",dir,"-l"],stdout=subprocess.PIPE)
        if result:
            print(result.stdout.decode('utf-8'))
        
            
    try:
        result = subprocess.run(["java","--version"],stdout=subprocess.PIPE)
        if result:
            print("JAVA=",result.stdout.decode('utf-8'))
        else:
            print("no available java")
    except Exception as e:
        print(e)
    
    result = subprocess.run(["pwd"],stdout=subprocess.PIPE)
    if result:
        print("pwd=",result.stdout.decode('utf-8'))
    
    
######################################################################
def add_widgets():                                           
    if st.button('run validation'):                        
        output = st.empty()
        with st_capture(output.code):
            run_validation(['/project/xml'])
        
            