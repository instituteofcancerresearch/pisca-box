import streamlit as st
import streamlit.components.v1 as components
import widgets
import os
import xml_gen as xg
from io import StringIO


def add_widgets():
    
    uploaded_file = st.file_uploader("Select fasta file",type=['fasta','fa'])                            
    if uploaded_file is not None:                                
        string_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        with st.expander("fasta file"):
            st.code(string_data)
                    
    cha = st.radio('Select something:', ["Choice A", "Choice B"],key="b2")
        
    option = st.selectbox('What clock model would you like?', ('strict', 'ancestral', 'discrete'),key="bb2")
    if cha and option:
        st.write('You selected:', option,cha)    
        st.divider()        
                                
        my_xml = xg.get_base_xml("","")
        with st.expander("View generated xml"):
            st.code(my_xml)
        
                
        js = widgets.get_saveas(my_xml)
        components.html(js, height=30)
            