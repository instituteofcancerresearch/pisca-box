import __init__
import streamlit as st

def add_widgets():   
    st.write("The containerisation and adaption of pisca-beast is a collaboration between the Institute of Cancer Research and Arizona State University.")
    st.markdown("[BEAST](http://beast.community/) was created .... some history")    
    st.markdown("[PISCA](https://github.com/adamallo/PISCA) was created by Diego Mallo .... some history")            
    st.markdown("[pisca-box](https://github.com/rachelicr/pisca-box) was created by Heather Grant and Rachel Alcraft .... some history")            
    st.divider()
    st.markdown("**Arizona State University**")
    
    st.write("[Diego Mallo](mailto:???), postdoctoral researcher in the Biodesign Institute")
    st.divider()
        
    from PIL import Image
    image = Image.open('app/static/icr.png')
    st.image(image)
    st.markdown('<span style="color:yellowgreen">Institute</span><span style="color:orange"> of</span><span style="color:hotpink"> Cancer</span><span style="color:darkred"> Research</span>', unsafe_allow_html=True)        
    
    st.write("[Heather Grant](mailto:heather.grant@icr.ac.uk), postdoctoral researcher in GEDy lab")
    st.write("[Rachel Alcraft](mailto:rachel.alcraft@icr.ac.uk), research software engineer in Scientific Computing")
    
    
    
    