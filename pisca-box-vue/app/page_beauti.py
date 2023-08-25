import streamlit as st
import streamlit.components.v1 as components
import widgets
import os
import pandas as pd
import gen_xml as xg
from io import StringIO
import cls_xml as xml
import cls_fasta as fa
import cls_mcmc as mc

#https://dev.to/chrisgreening/complete-list-of-markdown-emojis-for-your-blog-posts-and-readme-s-164j


def add_widgets():
    
    #cfa = st.container()
    fa_dates = None
    fa_data = ""   
    with st.container():
        st.subheader("Alignment")
        #col1, col2 = st.columns(2)
        with st.container():
        #with col1:            
            uploaded_file = st.file_uploader("Select fasta file",type=['fasta','fa'])                            
            if uploaded_file is not None:
                fa_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()        
                #with st.expander("expand fasta file to view"):
                #    st.code(fa_data)                
        #with st.container():
        #with col2:
            #if uploaded_file is not None:
            #    uploaded_dates = st.file_uploader("Select dates file",type=['csv'])                            
            #    if uploaded_dates is not None:
            #        fa_dates = pd.read_csv(uploaded_dates)
            #        #fa_dates = StringIO(uploaded_dates.getvalue().decode("utf-8")).read()
            #        with st.expander("expand dates file to view"):
            #            st.write(fa_dates)
    
    if uploaded_file is not None:
        
        tabAlign,tabDates, tabClock, tabLuca, tabGenerate = st.tabs(["alignment","dates","clock","luca","generate xml"])
        
        with tabAlign:
            st.subheader("Alignment file viewer")        
            with st.expander("expand fasta file to view"):
                st.code(fa_data)                
        
        with tabDates:
            st.subheader("Alignment dates")        
            uploaded_dates = st.file_uploader("Select dates file",type=['csv'])                            
            if uploaded_dates is not None:
                fa_dates = pd.read_csv(uploaded_dates)                    
                with st.expander("expand dates file to view"):
                    st.write(fa_dates)
                                                            
        with tabClock:
            st.subheader("Clock model")
            clock = st.radio('Select clock model:', ["strict clock", "random local clock"],key="cl")                    
            #clock = st.selectbox('What clock model would you like?', ('strict', 'ancestral', 'discrete'),key="bb2")
                
        with tabLuca:
            st.subheader("Luca Height and Branch")
            with st.container():
                col1, col2, col3 = st.columns(3)            
                with col1:                
                    lh_val = st.number_input(label="luca-height",value=5.0)
                with col2:                
                    lh_up = st.number_input(label="luca-height upper",value=60.0)
                with col3:                
                    lh_low = st.number_input(label="luca-height lower",value=5.0)
            with st.container():
                col1, col2, col3 = st.columns(3)
                with col1:                
                    lb_val = st.number_input(label="luca-branch",value=1.0)
                with col2:                
                    lb_up = st.number_input(label="luca-branch upper",value=55.0)
                with col3:                
                    lb_low = st.number_input(label="luca-branch lower",value=0.0)
            lucas = (lh_val,lh_up,lh_low,lb_val,lb_up,lb_low)
            
    
        ################################################################             
        with tabGenerate:
            st.write("#### :checkered_flag: Check and save xml")        
            ################################################################                                                          
            fasta = fa.Fasta(fa_data,fa_dates)
            mcmc = mc.MCMC("name")        
            xmlwriter = xml.XmlWriter(fasta,mcmc,lucas,clock)
            
            tst_xml = xmlwriter.get_xml()
            with st.expander("View generated xml"):
                st.code(tst_xml)        
            my_xml = xg.get_base_xml("","")
            with st.expander("View fixed xml to save"):
                st.code(my_xml)        
            ################################################################                                                          
            js = widgets.get_saveas(my_xml)
            components.html(js, height=30)
                