import __init__ # noqa: F401
import streamlit as st
import libs.widgets as widgets
import libs.temps as temps
import os

def add_widgets(include_header):
    if include_header:
        widgets.page_header('pisca admin')
            
    st.divider()
    st.write("Admininstration of webserver")
    st.write(f"Session ID={temps.get_session_id()}")
    your_name = st.text_input("Enter the admin password", "")
    if your_name in ["user","admin"]:
        st.write(f"Hello {your_name}")
        #names_entered = 1
        #if "names_entered" in st.session_state:
        #    names_entered = st.session_state["names_entered"] + 1
        #st.session_state["names_entered"] = names_entered
        
        #st.session_state[f'name_{names_entered}'] = your_name
        
        st.divider()
        st.write("Total session state")
        for k,v in st.session_state.items():
            st.write(f"{k}\t\t{v}")
            
        
        st.divider()
        st.write("Expand session temp files")
        for fl in temps.get_temp_list():
            if os.path.isfile(fl):
                with open(fl) as f:
                    ops_str = f.read()
                with st.expander(f"Expand {fl}"):
                    st.code(ops_str)
                    
        st.divider()
        st.write("All temp files")
        fls = temps.get_temp_files()
        for fl in fls:
            if "make.txt" not in fl:
                st.write(fl)
            
        
        if your_name == "admin":
            st.divider()
            if st.button("Clear temp files"):
                temps.delete_temp_files()                
                st.write("All temp files removed")
            
        



