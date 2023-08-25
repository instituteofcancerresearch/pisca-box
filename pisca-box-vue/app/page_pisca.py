import streamlit as st
import subprocess
import os
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import StringIO
from time import sleep
#import cmds_tst as cmd
import cmds as cmd

IS_TEST = False

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
    
######################################################################
def add_widgets():   
        
    st.write("#### :leaves: Choose an xml file")
    uploaded_file = st.file_uploader("upload xml file",type=['xml'])                            
    if uploaded_file is not None:                                
        string_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        full_file_name = "temp.xml"
        with open(full_file_name,"w") as fw:
            fw.write(string_data)
                                                        
        
        if os.path.isfile(full_file_name):
            #st.caption(f"{full_file_name} is a valid file")
            st.write("#### :leaves: Input parameters for beast")
            params_input = st.text_input("Enter additional parameters",value="-beagle_off")
            st.write("#### :leaves: Check inputs and run beast")
            if st.button('run pisca-box'):                        
                output = st.empty()
                params = []
                if params_input != "":
                    params = params + params_input.split(" ")
                    for pm in params:
                        if pm not in params and len(pm) > 2:
                            params.append(pm)
                params2 = ["-working", "-overwrite",full_file_name]                
                for pm in params2:
                    if pm not in params and len(pm) > 2:
                        params.append(pm)
                with st_capture(output.code):
                    cmd.run_beast(params)
        else:
            st.error(f"{full_file_name} is not a valid file, please check the working directory")
            result = subprocess.run(["ls","-l"],stdout=subprocess.PIPE)
            if result:
                st.error("These are the available files:")
                st.error(result.stdout.decode('utf-8'))
            