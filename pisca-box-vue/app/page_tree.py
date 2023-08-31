import streamlit as st
import streamlit.components.v1 as components
import widgets
import os
import pandas as pd
import gen_xml as xg
from io import StringIO
import cls_xml as xml
import cls_fasta as fa
import cls_mcmc as mc
from contextlib import contextmanager, redirect_stdout, redirect_stderr
import cmds as cmd

#https://dev.to/chrisgreening/complete-list-of-markdown-emojis-for-your-blog-posts-and-readme-s-164j

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
        
def add_widgets():
        
    log_out = None
    tree_out = None
                
    st.subheader("Phylogenetic tree")
    col1, col2 = st.columns(2)    
    with col1:            
        uploaded_file = st.file_uploader("Select log file",type=['log','log'])                            
        if uploaded_file is not None:
            log_out = StringIO(uploaded_file.getvalue().decode("utf-8")).read()        
            with st.expander("expand log file to view"):
                st.code(log_out)                    
    with col2:        
        uploaded_file = st.file_uploader("Select tree file",type=['trees','trees'])                            
        if uploaded_file is not None:            
            tree_out = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            with st.expander("expand tree file to view"):
                st.code(tree_out)
    
    if log_out is not None and tree_out is not None:
        st.subheader("Plot phylogenetic tree")
        burnin = st.number_input(label="burnin",value=100)
        ret = ""
        if st.button('run tree-annotation'):                        
            output = st.empty()            
            with st_capture(output.code):
                ret  = cmd.run_tree(log_out,tree_out,burnin,"out.trees")
            if ret == "done":
                new_tree = ""
                if os.path.isfile("out.trees"):
                    with open("out.trees") as f:
                        new_tree = f.read()
                with st.expander("expand new tree file to view"):
                    st.code(new_tree)
                
                with open("tmp.log", "w") as text_file:
                    text_file.write(log_out)
                log_csv = pd.read_csv("tmp.log",sep="\t",header=3)
                                
        