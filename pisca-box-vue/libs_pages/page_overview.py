import __init__ # noqa: F401
import streamlit as st
import libs.widgets as widgets

def add_widgets(include_header):
    if include_header:
        widgets.page_header('pisca overview')
        
    st.header('**Overview of PISCA**')      
    widgets.show_pdf('app/static/pisca-help-using-containers.pdf',height=800)
