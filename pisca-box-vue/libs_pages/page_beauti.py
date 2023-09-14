import __init__ # noqa: F401
import streamlit as st
import streamlit.components.v1 as components
import libs.widgets as widge
import pandas as pd
from io import StringIO
import libs.cls_xml as xml
import libs.cls_fasta as fa
import libs.cls_mcmc as mc
import libs.widgets as widgets

#https://dev.to/chrisgreening/complete-list-of-markdown-emojis-for-your-blog-posts-and-readme-s-164j




def add_widgets(include_header):
    if include_header:
        widgets.page_header('beauti-box')    
    uploaded_ages = None    
    seq_data = ""
    seq_csv = pd.DataFrame()
    with st.container():
        convert_from_csv = False
        st.subheader("Alignment")
        col1, col2 = st.columns([1,6])
        with col1:
            st.write('fasta format')
        with col2:
            convert_from_csv = st.toggle('csv format',value=False)
        
        if convert_from_csv:
            msg1,type1 = "Select sequence csv file",['csv']            
            msg2,type2 = "Select ages (dates/time) file",['csv']
        else:
            msg1,type1 = "Select fasta file",['fasta','fa']            
            msg2,type2 = "Select ages (dates/time) file",['csv']
        
        col1, col2 = st.columns(2)        
        with col1:            
            uploaded_file = st.file_uploader(msg1,type=type1)
            if uploaded_file is not None:
                if convert_from_csv:
                    seq_csv = pd.read_csv(uploaded_file)
                    with st.expander("expand sequence file to view"):
                        st.write(seq_csv)                        
                else:
                    seq_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()        
                    with st.expander("expand sequence file to view"):
                        st.code(seq_data)                        
        with col2:
            if uploaded_file is not None:
                uploaded_ages = st.file_uploader(msg2,type=type2)
                if uploaded_ages is not None:
                    seq_ages = pd.read_csv(uploaded_ages)
                    #fa_dates = StringIO(uploaded_dates.getvalue().decode("utf-8")).read()
                    with st.expander("expand ages file to view"):
                        st.write(seq_ages)
    
    if uploaded_ages is not None:
        # we need the luca branch values from the ages file
        if 'age' not in seq_ages.columns:
            st.error("The ages file must have a column called 'age'")
        else:
            max_age = seq_ages['age'].max()   
            min_age = seq_ages['age'].min()
                                    
            tabPisca, tabClock, tabLuca, tabTrees, tabMcmc, tabPriors,tabGenerate = st.tabs(["pisca","clock","luca","trees","mcmc","priors","generate xml"])
                                                                                
            ### PISCA ########################################################
            with tabPisca:
                datatypedic = {'absolute copy number alterations': 'acna', 'copy number variant': 'cnv', 'biallelic binary':'bb'}
                values = list(datatypedic.keys())
                datatypelong = st.radio('Select pisca datatype:', values,key="pisca")
                datatype = datatypedic[datatypelong]
                seq_conversion = datatype in ['cnv','acna']            
                #seq_conversion = st.checkbox("Convert to letters",value=True,help="If the sequence is entered as numbers, do you want to convert it to A-J?")
                
            ### CLOCK ########################################################
            with tabClock:
                st.subheader("Clock model")
                clock = st.radio('Select clock model:', ["strict clock", "random local clock"],key="cl")                    
                #clock = st.selectbox('What clock model would you like?', ('strict', 'ancestral', 'discrete'),key="bb2")
                    
            ### LUCA ########################################################
            with tabLuca:
                st.subheader("Luca Height and Branch")            
                with st.container():
                    cols = st.columns([5,1])            
                    with cols[0]:
                        lb_val = st.slider("luca-branch",0.0,min_age,min_age,help="This can be between 0 and the root node, or minimum age")
                    col1, col2 = st.columns([1,4])            
                    with col1:                
                        st.write(f"luca-height = {round(max_age,4)}")
                    with col2:
                        st.caption("This is total tree height, or maximum age")
                        
                    
                        
                lucas = (max_age,lb_val,min_age,0)
            
            ### TREES ########################################################
            with tabTrees:
                st.subheader("Demographic model")
                demographic = st.radio('Select demographic model:', ["constant size", "exponential growth"],key="dem")                    
                
            ### MCMC ########################################################
            with tabMcmc:
                st.subheader("MCMC model")
                col1, col2, col3 = st.columns(3)
                with col1:
                    name = st.text_input("Enter name",value="my_pisca")
                with col2:
                    chain_length = st.number_input(label="Chain length",value=2500)
                with col3:
                    log_every = st.number_input(label="Log every",value=250)
                    
            ### PRIORS ########################################################                        
            with tabPriors:
                cols = st.columns([1,1,1])
                with cols[0]:
                    st.write('clock rate')
                with cols[1]:
                    clock_mean = st.number_input(label="clock mean",value=5.0)
                with cols[2]:
                    clock_std = st.number_input(label="clock std",value=5.0)
                
                if clock_mean == clock_std:
                    print("same") #this is just debug code to stop the error about not being used in ruff for now
            
            ### GENERATE #############################################################             
            with tabGenerate:
                st.write("#### :checkered_flag: Check and save xml")        
                ################################################################                                                          
                fasta = fa.Fasta(seq_data,seq_ages,seq_conversion,seq_csv)
                mcmc = mc.MCMC(name,chain_length, log_every,clock)        
                xmlwriter = xml.XmlWriter(fasta,mcmc,lucas,clock,demographic,datatype)
                
                my_xml = xmlwriter.get_xml()            
                with st.expander("View generated xml"):
                    st.code(my_xml)                    
                ################################################################                                                          
                js = widge.get_saveas(my_xml,name)
                components.html(js, height=30)
                                            