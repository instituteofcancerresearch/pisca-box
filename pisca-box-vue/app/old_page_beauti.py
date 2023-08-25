import streamlit as st
import streamlit.components.v1 as components
import widgets
import os
import xml_gen as xg


def add_widgets():
    cha = st.radio('Select something:', ["Choice A", "Choice B"],key="a")
        
    option = st.selectbox('What clock model would you like?', ('strict', 'ancestral', 'discrete'))
    if cha and option:
        st.write('You selected:', option,cha)    
        st.divider()
        st.write("Save the xml to the working directory")
        working_dir = st.text_input('working directory:', '/project/xml/',key="beati_dir")
        if working_dir[-1] != "/":
            working_dir += "/"
        
        file_name = st.text_input('filename:', 'my_pisca.xml',key="beati_fl")
        
        xml = xg.get_base_xml("","")
        my_xml = st.text_area(xml)
        
        full_file_name = working_dir + file_name
        if st.button('save beauti-xml for pisca'):                        
            try:
                with open(full_file_name,"w") as fw:
                    fw.write(my_xml)
                st.write(f"Written xml file to {full_file_name}")
            except Exception as e:
                st.write(f"Error writing file to {full_file_name} {e}")
                        
        
        #js = widgets.get_saveas(xml)
        #components.html(js, height=30)
            