import __init__ # noqa: F401
import streamlit as st
import libs.widgets as widgets

def add_widgets(include_header):
    if include_header:
        widgets.page_header('pisca overview')
        
    st.header('**PISCA Installation and Usage**')      
    widgets.show_pdf('app/static/pisca-help-install-use.pdf',height=800)
