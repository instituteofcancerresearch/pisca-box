import streamlit as st
import pandas as pd
import numpy as np
import os
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from time import sleep
import page_beauti as pageBe
import page_about as pageAb
import page_home as pageHm
import page_help as pageHe

import cmds0 as cmd

st.set_page_config(page_title='pisca-box', page_icon = None, layout = 'wide', initial_sidebar_state = 'auto')
# favicon being an object of the same kind as the one you should provide st.image() with (ie. a PIL array for example) or a string (url or local file path)
st.title('Pisca-Box')

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




# Insert containers separated into tabs:
tabHm, tabPB, tabBB, tabHlp,tabAb = st.tabs(["home","pisca-box","beauti-box","help","about"])

with tabHm:
    pageHm.add_widgets()    
with tabBB:
    pageBe.add_widgets()    
with tabAb:
    pageAb.add_widgets()
with tabHlp:
    pageHe.add_widgets()
    
with tabPB:
    uploaded_file = st.file_uploader("Choose a file",type=['xml'])
    if uploaded_file is not None:
        file_name = os.path.realpath(uploaded_file.name)
        if st.button('run pisca-box'):
            st.write('Why hello there')                
            output = st.empty()
            with st_capture(output.code):
                print("Hello")
                sleep(1)
                print("World")
            
            output2 = st.empty()
            with st_capture(output2.code):
                cmd.run_beast("",[],True)

        