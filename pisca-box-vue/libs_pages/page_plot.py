import __init__ # noqa: F401
import streamlit as st
import libs.cmds as cmd
import libs.widgets as widgets
from contextlib import contextmanager, redirect_stdout
from io import StringIO
import pandas as pd
import os


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

def add_widgets(include_header):
    if include_header:
        widgets.page_header('beauti-box')
            
    with st.container():
        st.write("#### Plot consensus tree")
        msg1,type1 = "Select consesus tree",['tree','mcc']
        msg2,type2 = "Select tree logs",['log']
        lh = st.number_input(label="luca-height",value=1.00)
        
        flog,outtree = "",""
        if "flog" in st.session_state:            
            flog = st.session_state["flog"]
        if "outtree" in st.session_state:            
            outtree = st.session_state["outtree"]
                                
        log_csv = pd.DataFrame()
        if os.path.isfile(outtree):
            with open(outtree) as f:
                ops_str = f.read()
            with st.expander(f"Expand consensus tree {outtree}"):
                st.code(ops_str)        
        if os.path.isfile(flog):
            with open(flog) as f:
                log_str = f.read()
            log_csv = pd.read_csv(flog,sep="\t",header=3)
            with st.expander(f"Expand log file {flog}"):
                st.dataframe(log_csv)
            
        
        if os.path.isfile(outtree) and os.path.isfile(flog):
            if st.button('run r-script'):
                output = st.empty()
                with st_capture(output.code):
                    ret = cmd.run_r_script(outtree,flog,lh,"temp.svg","")
                    #ret = cmd.run_r_script(outtree,flog,lh,"temp.pdf","")
                    print(ret)
                if os.path.isfile("temp.svg"):
                    html_str = ""
                    with open("temp.svg", "r") as f:
                        html_str = f.read()
                    st.write(html_str, unsafe_allow_html=True)
            
            
                
        
        