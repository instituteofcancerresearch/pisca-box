import __init__ # noqa: F401
import streamlit as st
import libs_pages.page_beauti as pageBe
import libs_pages.page_home as pageHm
import libs_pages.page_pisca as pagePi
import libs_pages.page_tree as pageTv
import libs.widgets as widgets
import libs.temps as temps

tabs = False
if tabs:
    widgets.page_header(divider=True)
    tabHm, tabBB, tabPB, tabTv  = st.tabs(["home","beauti-box","pisca-box","tree-vue"])
    with tabHm:
        pageHm.add_widgets(False)
    with tabBB:
        pageBe.add_widgets(False)
    with tabPB:
        pagePi.add_widgets(False)
    with tabTv:
        pageTv.add_widgets(False)
else:
    pageHm.add_widgets(True)
    
st.divider()

    
    