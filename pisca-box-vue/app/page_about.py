import __init__ # noqa: F401
import streamlit as st
from PIL import Image

def add_widgets():       
    image = Image.open('app/static/icr.png')
    st.markdown("""
                
                The containerisation and adaption of pisca-beast is a collaboration between the Institute of Cancer Research and Arizona State University.
                
                [BEAST](http://beast.community/) was created .... some history  
                [PISCA](https://github.com/adamallo/PISCA) was created by Diego Mallo .... some history  
                [pisca-box](https://github.com/rachelicr/pisca-box) was created by Heather Grant and Rachel Alcraft .... some history  
                
                """)
    st.divider()
    st.markdown("""
                
                #### Collaborators
                **Arizona State University**  
                [Diego Mallo](mailto:???), postdoctoral researcher in the Biodesign Institute
                          
             """)                         
    
    st.image(image)
    st.markdown('<span style="color:yellowgreen">Institute</span><span style="color:orange"> of</span><span style="color:hotpink"> Cancer</span><span style="color:darkred"> Research</span>', unsafe_allow_html=True)        
    
    st.markdown("""
                
                [Heather Grant](mailto:heather.grant@icr.ac.uk), postdoctoral researcher in GEDy lab  
                [Rachel Alcraft](mailto:rachel.alcraft@icr.ac.uk), research software engineer in Scientific Computing
                
                """)
    
    
    
    
    