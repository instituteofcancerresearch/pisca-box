import streamlit as st



def add_widgets():
    cha = st.radio('Select something:', ["Choice A", "Choice B"],key="a")
        
    option = st.selectbox('What clock model would you like?', ('strict', 'ancestral', 'discrete'))
    st.write('You selected:', option,cha)
    