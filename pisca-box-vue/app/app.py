import streamlit as st
import pandas as pd
import numpy as np
import os
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import StringIO
from time import sleep
import page_beauti as pageBe
import page_beauti2 as pageBe2
import page_about as pageAb
import page_home as pageHm
import page_help as pageHe
import page_pisca as pagePi
import page_pisca2 as pagePi2
import page_test as pageTs

st.set_page_config(page_title='pisca-box', page_icon = None, layout = 'wide', initial_sidebar_state = 'auto')
# favicon being an object of the same kind as the one you should provide st.image() with (ie. a PIL array for example) or a string (url or local file path)
st.title('Pisca-Box-Vue')


# Insert containers separated into tabs:
#tabHm, tabPB, tabBB, tabHlp, tabAb = st.tabs(["home","pisca-box","beauti-box","help","about"])
#tabHm, tabPB2, tabBB2, tabHlp, tabAb, tabTs = st.tabs(["home","pisca-box","beauti-box","help","about","(test)"])
tabHm, tabPB2, tabBB2, tabHlp, tabAb = st.tabs(["home","pisca-box","beauti-box","help","about"])

with tabHm:
    pageHm.add_widgets()    
#with tabBB:
#    pageBe.add_widgets()    
with tabBB2:
    pageBe2.add_widgets()    
with tabAb:
    pageAb.add_widgets()
with tabHlp:
    pageHe.add_widgets()    
#with tabPB:
#    pagePi.add_widgets()
with tabPB2:
    pagePi2.add_widgets()        
#with tabTs:
#    pageTs.add_widgets()
    