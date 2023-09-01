import streamlit as st
import subprocess
import os
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import StringIO
from time import sleep
#import cmds_tst as cmd
import cmds as cmd
import pandas as pd
import widgets
import streamlit.components.v1 as components

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
        
    st.subheader("Choose an xml file")
    uploaded_file = st.file_uploader("upload xml file",type=['xml'])                            
    if uploaded_file is not None:                                
        string_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        full_file_name = "temp.xml"
        with open(full_file_name,"w") as fw:
            fw.write(string_data)
                                                        
        
        if os.path.isfile(full_file_name):
        
            st.subheader("Input parameters")
            col1,col2 = st.columns(2)
            with col1:
                params_input = st.text_input("Enter additional beast parameters",value="-beagle_off")
            with col2:
                burnin = st.number_input(label="Enter annotation burnin",value=100)
            st.subheader("Check inputs and run")
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
                ret = ""
                
                with st_capture(output.code):
                    ret  = cmd.run_beast(params)
                    #str = cmd.run_validation(["/project","/project/xml","/mnt"])
                    #print(str)                    
                    if ret == "done":                        
                        flog = cmd.get_logs(string_data,".log")
                        fops = cmd.get_logs(string_data,".ops")
                        ftree = cmd.get_logs(string_data,".trees")
                        
                        if os.path.isfile(fops):
                            with open(fops) as f:
                                ops_str = f.read()
                        if os.path.isfile(ftree):
                            with open(ftree) as f:
                                tree_str = f.read()
                        if os.path.isfile(flog):
                            with open(flog) as f:
                                log_str = f.read()
                        log_csv = pd.read_csv(flog,sep="\t",header=3)
                        
                        
                        nm,ext = ftree.split(".")
                        fano = nm + "_annotated." + ext
                        ret  = cmd.run_tree(tree_str,burnin,fano)
                        if os.path.isfile(fano):
                            with open(fano) as f:
                                ano_str = f.read()
                                                                
                
                
                col1,col2 = st.columns(2)
                with col1:
                    nm,ext = fops.split(".")
                    js = widgets.get_saveas(ops_str,nm,ext,"Save ops")
                    components.html(js, height=30)                                                                            
                    with st.expander(f"view ops file {fops}"):                                        
                        st.code(ops_str)
                
                with col2:
                    nm,ext = flog.split(".")
                    js = widgets.get_saveas(log_str,nm,ext,"Save log")
                    components.html(js, height=30)   
                    with st.expander(f"view log file {flog}"):                                        
                        st.write(log_csv)
                
                col3,col4 = st.columns(2)
                with col3:        
                    nm,ext = ftree.split(".")
                    js = widgets.get_saveas(tree_str,nm,ext,"Save tree")
                    components.html(js, height=30)                
                    with st.expander(f"view tree file {ftree}"):                                        
                        st.code(tree_str)
                                        
                with col4:        
                    nm,ext = fano.split(".")
                    js = widgets.get_saveas(ano_str,nm,ext,"Save annotated tree")
                    components.html(js, height=30)   
                    with st.expander(f"view annotated tree {fano}"):                                        
                        st.code(ano_str)
                                                                    
        else:
            st.error(f"{full_file_name} is not a valid file, please check the working directory")
            result = subprocess.run(["ls","-l"],stdout=subprocess.PIPE)
            if result:
                st.error("These are the available files:")
                st.error(result.stdout.decode('utf-8'))
            