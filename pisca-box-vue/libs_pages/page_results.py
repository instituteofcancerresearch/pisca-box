import __init__ # noqa: F401
import streamlit as st
import os

#import cmds_tst as cmd

import pandas as pd
import libs.widgets as widgets

IS_TEST = False

    
######################################################################
def add_widgets(include_header):
    if include_header:
        widgets.page_header('pisca-box')
        
    st.subheader("Results from pisca-box")
                
    ops_str,tree_str,log_str = "","",""
     
    if "flog" not in st.session_state:
        st.write("No data has been run yet")
    else:
        flog,fops,ftree = "","",""
        if "flog" in st.session_state:
            flog = st.session_state["flog"]
        if "fops" in st.session_state:
            fops = st.session_state["fops"]
        if "ftree" in st.session_state:
            ftree = st.session_state["ftree"]
                                                        
        log_csv = pd.DataFrame()
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
                                                                    
        with st.expander("expand trees"):
            st.code(tree_str)    
        st.download_button("Download trees",tree_str,file_name="pisca.trees")
                
        with st.expander("expand ops"):
            st.code(ops_str)        
        st.download_button("Download ops",ops_str,file_name="pisca.ops")
                
        with st.expander("expand log"):
            st.write(log_csv)        
        st.download_button("Download log",log_str,file_name="pisca.log")
        st.divider()
                                                                                            
        
            
                        
                        
                                                    
                