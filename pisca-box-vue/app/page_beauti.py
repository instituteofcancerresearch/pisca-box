import streamlit as st
import streamlit.components.v1 as components
import widgets



def add_widgets():
    cha = st.radio('Select something:', ["Choice A", "Choice B"],key="a")
        
    option = st.selectbox('What clock model would you like?', ('strict', 'ancestral', 'discrete'))
    st.write('You selected:', option,cha)    
    file_name = "from_box.xml"    
    xml = "<some xml to save>"                
    js = widgets.get_saveas(xml)
    components.html(js, height=30)
        