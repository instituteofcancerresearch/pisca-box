import __init__ # noqa: F401
import streamlit as st
import os
from io import StringIO
#import cmds_tst as cmd
import libs.cmds as cmd

import libs.widgets as widgets
import libs.temps as temps

import libs.callback as cb

IS_TEST = False

    
######################################################################
def add_widgets(include_header):
    if include_header:
        widgets.page_header('pisca-box')
        
    st.subheader("Choose an xml file")
    output = st.empty()
    uploaded_file = st.file_uploader("upload xml file",type=['xml'])
    if uploaded_file is not None:
        string_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        
        new_flog = temps.get_pisca_flog()
        new_fops = temps.get_pisca_ops()
        new_trees = temps.get_pisca_trees()            
        string_data = cmd.change_logs(string_data,"fileName=",".log",new_flog)
        string_data = cmd.change_logs(string_data,"operatorAnalysis=",".ops",new_fops)
        string_data = cmd.change_logs(string_data,"fileName=",".trees",new_trees)
                            
        full_file_name = temps.get_pisca_temp()
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
                output = st.empty()
                with cb.st_capture(output.code,temps.get_session_id()):
                    ret  = cmd.run_beast(params)
                        #ret  = dkr.beast_docker(full_file_name,docker_params,docker_version)
                        #str = cmd.run_validation(["/project","/project/xml","/mnt"])
                        #print(str)
                if ret == "done":
                    st.write("pisca-box run complete")                    
                    flog = "temp/"+cmd.get_logs(string_data,".log")
                    fops = "temp/"+cmd.get_logs(string_data,".ops")
                    ftree = "temp/"+cmd.get_logs(string_data,".trees")
                    
                    st.session_state["flog"] = flog
                    st.session_state["fops"] = fops
                    st.session_state["ftree"] = ftree                                                                                        
                else:
                    st.error("The BEAST application failed")
                    
                    
                                                
                