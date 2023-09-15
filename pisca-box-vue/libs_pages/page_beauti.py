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
                    seq_csv = pd.read_csv(uploaded_file,index_col=0)
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
                cols = st.columns([1,1])
                with cols[0]:
                    clock = st.radio('Select clock model:', ["strict clock", "random local clock"],key="cl")                                    
                with cols[1]:
                    clock_rate = st.number_input(label="clock rate",value=1.00)                    
                clocks = {}        
                clocks['type'] = clock
                clocks['rate'] = clock_rate
                    
            ### LUCA ########################################################
            with tabLuca:
                st.subheader("Luca Height and Branch")            
                with st.container():
                    cols = st.columns([5,1])            
                    with cols[0]:
                        lb_val = st.slider("luca-branch",0.0,min_age,float(round(min_age/2)),help="This can be between 0 and the root node, or minimum age")
                    col1, col2 = st.columns([1,4])            
                    with col1:                
                        st.write(f"luca-height = {round(max_age,4)}")
                    with col2:
                        st.caption("This is total tree height, or maximum age")
                                                                                    
                lucas = {}
                lucas["height"] = max_age
                lucas["branch"] = lb_val
                lucas["lower"] = 0.0
                lucas["upper"] = min_age                
            
            ### TREES ########################################################
            with tabTrees:
                st.subheader("Demographic model")
                demographic = st.radio('Select demographic model:', ["constant size", "exponential growth"],key="dem")                    
                
            ### MCMC ########################################################
            with tabMcmc:
                mcmcs = {}
                st.subheader("MCMC model")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    name = st.text_input("Enter name",value="my_pisca")
                with col2:
                    chain_length = st.number_input(label="Chain length",value=2500)
                with col3:
                    log_every = st.number_input(label="Log every",value=250)
                with col4:
                    st.write("Marginal Likehood Estimation")
                    mle = st.toggle('mle',value=False)
                mcmcs['name'] = name
                mcmcs['chain_length'] = chain_length
                mcmcs['log_every'] = log_every
                mcmcs['mle'] = mle
                                    
            ### PRIORS ########################################################                        
            with tabPriors:
                prior_types = ['oneOnX', 'logNormal', 'normal','exponential','uniform','laplace']
                priors = {}
                with st.expander("View or change standard priors"):
                    luca_priors = st.checkbox("Luca priors",value=True,help="Do you want to set priors on the luca branches?")
                    if luca_priors:
                        prior_id = ''
                        cols = st.columns([1,1,1])
                        with cols[0]:                        
                            prior_type = st.selectbox('prior type', prior_types,key="luca",index=4)
                        with cols[1]:
                            height_branch = st.radio('height or branch', ["height", "branch"],key="hb")
                        with cols[2]:
                            luca_val = st.number_input(label="luca height prior",value=round(max_age,4))
                        if height_branch == 'height':
                            prior_id = "luca_height"
                        else:
                            prior_id = "luca_branch"
                        priors[prior_id] = {'prior_type':prior_type,'value':luca_val,}  
                    
                if datatype == 'bb':
                    with st.expander("View or change biallelic binary priors"):
                        bb_priors = st.checkbox("Biallelic binary priors",value=datatype=='bb',help="Do you want to set priors on the biallelic binary?")
                        if bb_priors:
                            st.write('demethylation')
                            de_realSpace = True#st.checkbox("demethylation in real space",value=True)
                            cols = st.columns([1,1,1,1])                            
                            with cols[0]:
                                de_type = st.selectbox('prior type', prior_types,key="de",index=1)
                            with cols[1]:
                                de_mean = st.number_input(label="mean",value=1.0,key="de_mean")
                            with cols[2]:
                                de_std = st.number_input(label="std",value=0.6,key="de_std")
                            with cols[3]:
                                de_offset = st.number_input(label="offset",value=0.0,key="de_offset")
                                
                            st.write('homozygousMethylation')                                                        
                            ho_realSpace = True#st.checkbox("homozygousMethylation in real space",value=True)
                            cols = st.columns([1,1,1,1])
                            with cols[0]:
                                ho_type = st.selectbox('prior type', prior_types,key="ho",index=1)
                            with cols[1]:
                                ho_mean = st.number_input(label="mean",value=1.0,key="ho_mean")
                            with cols[2]:
                                ho_std = st.number_input(label="std",value=0.6,key="ho_std")
                            with cols[3]:
                                ho_offset = st.number_input(label="offset",value=0.0,key="ho_offset")
                                
                            st.write('homozygousDemethylation')
                            ho2_realSpace = True#st.checkbox("homozygousDemethylation in real space",value=True)    
                            cols = st.columns([1,1,1,1])
                            with cols[0]:
                                ho2_type = st.selectbox('prior type', prior_types,key="ho2",index=1)
                            with cols[1]:
                                ho2_mean = st.number_input(label="mean",value=1.0,key="ho2_mean")
                            with cols[2]:
                                ho2_std = st.number_input(label="std",value=0.6,key="ho2_std")
                            with cols[3]:
                                ho2_offset = st.number_input(label="offset",value=0.0,key="ho2_offset")
                            
                                                                                            
                            priors['biallelicBinary.demethylation'] = {'prior_type':de_type,'mean':de_mean,'std':de_std,'offset':de_offset,'realSpace':de_realSpace}
                            priors['biallelicBinary.homozygousMethylation'] = {'prior_type':ho_type,'mean':ho_mean,'std':ho_std,'offset':ho_offset,'realSpace':ho_realSpace}
                            priors['biallelicBinary.homozygousDemethylation']= {'prior_type':ho2_type,'mean':ho2_mean,'std':ho2_std,'offset':ho2_offset,'realSpace':ho2_realSpace}    
                    
                with st.expander("View or change other priors"):
                    clock_priors = st.checkbox("Clock priors",value=False,help="Do you want to set priors on the clock rate?")
                    if clock_priors:
                        cols = st.columns([1,1,1,1])
                        with cols[0]:                        
                            prior_type = st.selectbox('prior type', prior_types,key="clock",index=2)
                        with cols[1]:
                            st.write('clock rate')
                            st.write(clock_rate)
                        with cols[2]:
                            clock_mean = st.number_input(label="clock mean",value=0.0)
                        with cols[3]:
                            clock_std = st.number_input(label="clock std",value=0.1)                    
                        priors['clock.rate'] = {'prior_type':prior_type,'mean':clock_mean,'std':clock_std}
                                            
            ### GENERATE #############################################################             
            with tabGenerate:
                st.write("#### :checkered_flag: Check and save xml")        
                ################################################################                                                          
                fasta = fa.Fasta(seq_data,seq_ages,seq_conversion,seq_csv)
                mcmc = mc.MCMC(mcmcs,clocks,priors)        
                xmlwriter = xml.XmlWriter(fasta,mcmc,lucas,clocks,demographic,datatype)
                
                my_xml = xmlwriter.get_xml()            
                                                                    
                with st.expander("View generated xml"):
                    my_xml = st.text_area('Edit xml if necessary, tab out to inactivate box before saving',value=my_xml,height=400)
                ################################################################                                                          
                js = widge.get_saveas(my_xml,name)
                components.html(js, height=30)
                
                                            