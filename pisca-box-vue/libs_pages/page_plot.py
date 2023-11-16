import __init__ # noqa: F401
import streamlit as st
from streamlit_ace import st_ace
import streamlit.components.v1 as components
import libs.widgets as widgets
import pandas as pd
from io import BytesIO


def add_widgets(include_header):
    if include_header:
        widgets.page_header('beauti-box')
            
    with st.container():
        st.write("#### Consensus Tree")
        msg1,type1 = "Select consesus tree",['tree','mcc']
        msg2,type2 = "Select tree logs",['log']
        lh = st.number_input(label="luca-height",value=1.00)
                
        uploaded_tree = st.file_uploader(msg1,type=type1,accept_multiple_files=False)
        if uploaded_tree is not None:
            with st.expander("expand consensus tree to view"):
                st.write(uploaded_tree)
                            
        uploaded_logs = st.file_uploader(msg2,type=type2)
        if uploaded_logs is not None:
            with st.expander("expand log file to view"):
                st.write(uploaded_logs)
        