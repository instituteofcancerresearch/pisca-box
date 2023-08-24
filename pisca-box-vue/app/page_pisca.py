import streamlit as st
import subprocess
import os
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import StringIO
from time import sleep
#import cmds0 as cmd
import cmds1 as cmd

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
    working_dir = st.text_input('working directory', '/project/xml/')
    if working_dir[-1] != "/":
        working_dir += "/"
    uploaded_file = st.file_uploader("Choose a file",type=['xml'])    
    if uploaded_file is not None:
        full_file_name = working_dir + uploaded_file.name                
        if os.path.isfile(full_file_name):
            st.caption(f"{full_file_name} is a valid file")
            if st.button('run pisca-box'):                        
                output = st.empty()
                params = ["-beagle_off", "-working", "-overwrite",full_file_name]
                with st_capture(output.code):
                    cmd.run_beast(params,IS_TEST)
        else:
            st.error(f"{full_file_name} is not a valid file, please check the working directory")
            result = subprocess.run(["ls",working_dir,"-l"],stdout=subprocess.PIPE)
            if result:
                st.error("These are the available files:")
                st.error(result.stdout.decode('utf-8'))
            