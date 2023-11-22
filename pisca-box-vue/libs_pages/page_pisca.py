import __init__ # noqa: F401
import streamlit as st
import os
from contextlib import contextmanager, redirect_stdout
from io import StringIO
#import cmds_tst as cmd
import libs.widgets as widge
import libs.cmds as cmd
import libs.docker as dkr

import pandas as pd
import streamlit.components.v1 as components
import libs.widgets as widgets

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
def add_widgets(include_header):
    if include_header:
        widgets.page_header('pisca-box')
        
    st.subheader("Choose an xml file")
    uploaded_file = st.file_uploader("upload xml file",type=['xml'])
    if uploaded_file is not None:
        string_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        full_file_name = "temp.xml"
        with open(full_file_name,"w") as fw:
            fw.write(string_data)
        
        with st.expander("Expand uploaded xml"):
            st.code(string_data)
                                                        
        
        if os.path.isfile(full_file_name):
        
            st.subheader("Input parameters")
            col1,col2 = st.columns(2)
            with col1:
                params_input = st.text_input("Enter additional beast parameters",value="-beagle_off")
            #with col2:
            #    docker_version = st.selectbox("Select a beast version",["pisca-box-run","pisca-branch-master"])
            #with col2:
            #    burnin = st.number_input(label="Enter annotation burnin",value=100)
            st.subheader("Check inputs and run")
            if st.button('run pisca-box'):
                output = st.empty()
                docker_params = ["-working", "-overwrite"]
                params = ["-working", "-overwrite"]
                if params_input != "":
                    input_params = params_input.split(" ")
                    for pm in input_params:
                        if pm not in params and len(pm) > 2:
                            params.append(pm)
                        if pm not in docker_params and len(pm) > 2:
                            docker_params.append(pm)
                params.append(full_file_name)
                ret = ""
                
                
                #with st_capture(output.code):
                with st_capture(output.code):
                    ret  = cmd.run_beast(params)
                        #ret  = dkr.beast_docker(full_file_name,docker_params,docker_version)
                        #str = cmd.run_validation(["/project","/project/xml","/mnt"])
                        #print(str)
                if ret == "done":
                    st.write("pisca-box run complete")                    
                    flog = cmd.get_logs(string_data,".log")
                    fops = cmd.get_logs(string_data,".ops")
                    ftree = cmd.get_logs(string_data,".trees")
                    
                    st.session_state["flog"] = flog
                    st.session_state["fops"] = fops
                    st.session_state["ftree"] = ftree                                                                                        
                else:
                    st.error("The BEAST application failed")
                    
                    
                                                
                