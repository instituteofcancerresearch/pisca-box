"""
import streamlit as st
import pandas as pd
import numpy as np

st.title('Pisca Beauti-Beast Box')



# Insert containers separated into tabs:
tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
tab1.write("this is tab 1")
tab2.write("this is tab 2")

with tab1:
    st.radio('Select one:', [1, 2])
    
with tab2:
    st.file_uploader('File uploader')
    
"""
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from time import sleep
import streamlit as st

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


output = st.empty()
with st_capture(output.code):
    print("Hello")
    sleep(1)
    print("World")

output = st.empty()
with st_capture(output.info):
    print("Goodbye")
    sleep(1)
    print("World")