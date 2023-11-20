import __init__ # noqa: F401
import streamlit as st
from streamlit_ace import st_ace
import streamlit.components.v1 as components
import libs.widgets as widge
import pandas as pd
import libs.cls_xml as xml
import libs.cls_dt_biallelic as bb
import libs.cls_dt_acna as ac
import libs.cls_dt_cnv as cv
import libs.cls_dt_phyfum as phy
import libs.cls_operators as ops
import libs.cls_priors as prs
import libs.cls_mcmc as mc
import libs.cls_datadetermine as dd
import libs.widgets as widgets
from io import BytesIO


#https://dev.to/chrisgreening/complete-list-of-markdown-emojis-for-your-blog-posts-and-readme-s-164j




def add_widgets(include_header):
    if include_header:
        widgets.page_header('beauti-box')
    
    #### Establish datatype before doing anythong else ##############################
    
    #### Alignment and ages data ###################################################
    uploaded_ages = None
    dt_obj = None
    
    ## create state of choices in the screen
    log_choices = []
        
    with st.container():
        st.write("#### Alignment")
        msg1,type1 = "Select fasta/csv file",['fasta','fa','csv']
        msg2,type2 = "Select ages (dates/time) file",['csv']
        
        source = st.radio('Select source:', ["local file", "sample data"],key="src")
        if source == "local file":
            col1, col2 = st.columns(2)
            with col1:
                uploaded_file = st.file_uploader(msg1,type=type1,accept_multiple_files=False)
                if uploaded_file is not None:
                    nm,tp = uploaded_file.name.lower().split(".")
                    dtd = dd.DataDetermine(uploaded_file,tp)
                    dic_seq,dtyp = dtd.get_seq_data()
                    with st.expander(f"expand {dtyp} sequence to view"):
                        st.write(dic_seq)
                        st.write(dtd.seq_data)
            with col2:
                if uploaded_file is not None:
                    uploaded_ages = st.file_uploader(msg2,type=type2)
                    if uploaded_ages is not None:
                        seq_ages = pd.read_csv(uploaded_ages)
                        #fa_dates = StringIO(uploaded_dates.getvalue().decode("utf-8")).read()
                        with st.expander("expand ages file to view"):
                            st.write(seq_ages)
        else:
            radio_source = st.radio('Select sample data type:', ["acna","cnv","biallelic","phyfum"],key="src_sample")
            # sequence data
            file_name = f"app/static/{radio_source}-seq.csv"
            typ = "csv"
            if radio_source == "cnv":
                file_name = f"app/static/{radio_source}-seq.fasta"
                typ = "fasta"
            with open(file_name, "rb") as fh:
                uploaded_file = BytesIO(fh.read())
            dtd = dd.DataDetermine(uploaded_file,typ)
            dic_seq,dtyp = dtd.get_seq_data()
            with st.expander(f"expand {dtyp} sequence to view"):
                st.write(dic_seq)
                st.write(dtd.seq_data)
            # ages data
            file_name = f"app/static/{radio_source}-ages.csv"
            with open(file_name, "rb") as fh:
                uploaded_ages = BytesIO(fh.read())
            seq_ages = pd.read_csv(uploaded_ages)
            with st.expander("expand ages file to view"):
                st.write(seq_ages)
                
            
    
    if uploaded_ages is not None:
        # we need the luca branch values from the ages file
        if 'age' not in seq_ages.columns:
            st.error("The ages file must have a column called 'age'")
        else:
            max_age = seq_ages['age'].max()
            min_age = seq_ages['age'].min()
                                    
            tabPisca, tabClock, tabLuca, tabTrees, tabMcmc, tabPriors,tabLog,tabGenerate = st.tabs(["pisca","clock","luca","trees","mcmc","priors","log","generate xml"])
                                                                                
            ### PISCA ########################################################
            with tabPisca:
                datatype_long = ['absolute copy number alterations',
                                'copy number variant',
                                'biallelic binary',
                                "bulk methylation"]
                datatype_short = ['acna','cnv','biallelic',"phyfum"]
                values = datatype_long
                idx = datatype_short.index(dtyp)
                datatypelong = st.radio('Select pisca datatype:', values,index=idx,key="pisca")
                idxl = datatype_long.index(datatypelong)
                dtyp = datatype_short[idxl]
                if dtyp == 'biallelic':
                    dt_obj =  bb.Biallelic(dic_seq,seq_ages)
                elif dtyp == 'acna':
                    dt_obj =  ac.Acna(dic_seq,seq_ages)
                elif dtyp == "cnv":
                    dt_obj =  cv.Cnv(dic_seq,seq_ages)
                elif dtyp == "phyfum":
                    dt_obj =  phy.Phyfum(dic_seq,seq_ages)
                else:
                    st.write("Unrecognised datatype",dtyp)
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
                    cols = st.columns([1,1,3])
                    with cols[0]:
                        st.write("luca-upper")
                    with cols[1]:
                        min_age = st.number_input(label="luca-upper",value=min_age,label_visibility="collapsed")
                    with cols[2]:
                        st.caption("This is first branch height, or minimum age")
                    cols = st.columns([1,1,3])
                    with cols[0]:
                        st.write("luca-height")
                    with cols[1]:
                        max_age = st.number_input(label="luca-height",value=max_age,label_visibility="collapsed")
                    with cols[2]:
                        st.caption("This is total tree height, or maximum age")
                    
                    cols = st.columns([5,1])
                    with cols[0]:
                        col0s = st.columns([4,1])
                        with col0s[0]:
                            lb_val = st.slider("luca-branch",
                                            value = float(round(min_age/2)),
                                            min_value = float(0),
                                            max_value = float(min_age),
                                            help="This can be between 0 and the root node, or minimum age")
                    
                    
                                                                                    
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
                    chain_length = st.number_input(label="Chain length",value=10000000)
                with col3:
                    log_every = int(st.number_input(label="Log every",value=int(chain_length)/10000))
                with col4:
                    st.write("Marginal Likehood Estimation")
                    mle = st.toggle('mle',value=False)
                mcmcs['name'] = name
                mcmcs['chain_length'] = chain_length
                mcmcs['log_every'] = log_every
                mcmcs['mle'] = mle
                                                            
            ### PRIORS ########################################################
            with tabPriors:
                prrs = prs.Priors(demographic,dt_obj.prs)
                                                
                prior_types = ['oneOnX', 'logNormal', 'normal','exponential','uniform','laplace']
                prh,prb = [],[]
                with st.expander("View or change luca priors"):
                    luca_priors = st.checkbox("Luca priors",value=True,help="Do you want to set priors on the luca branches?")
                    prh = ['uniform','luca_height',str(lb_val),str(max_age),'','','','','','','']
                    prb = ['uniform','luca_branch',str(lb_val),str(max_age),'','','','','','','']
                    if luca_priors:
                        cols = st.columns([1,1,1])
                        with cols[0]:
                            prior_type = st.selectbox('prior type', prior_types,key="luca",index=4)
                            prior_type += "Prior"
                        with cols[1]:
                            inc_height = st.checkbox("luca-height prior",value=True)
                            inc_branch = st.checkbox("luca-prior prior",value=False)
                        with cols[2]:
                            luca_val = st.number_input(label="luca prior",value=round(lb_val,4))
                        
                        prh = [prior_type,'luca_height',str(luca_val),str(max_age),'','','','','','','']
                        prb = [prior_type,'luca_branch',str(luca_val),str(max_age),'','','','','','','']
                        if inc_height:
                            prrs.update_one_prior(False,'luca_height',prh)
                        else:
                            prrs.update_one_prior(True,'luca_height',prh)
                            
                        if inc_branch:
                            prrs.update_one_prior(False,'luca_branch',prb)
                        else:
                            prrs.update_one_prior(True,'luca_branch',prb)
                            
                    else:
                        prrs.update_one_prior(True,'luca_height',prh)
                        prrs.update_one_prior(True,'luca_branch',prb)

                if dtyp == 'biallelic':
                    with st.expander("View or change biallelic binary priors"):
                        bb_priors = st.checkbox("Biallelic binary priors",value=dtyp=='biallelic',help="Do you want to set priors on the biallelic binary?")
                        b1_pr,b2_pr,b3_pr = [],[],[]
                        if bb_priors:
                            st.write('demethylation')
                            de_realSpace = True#st.checkbox("demethylation in real space",value=True)
                            cols = st.columns([1,1,1,1])
                            with cols[0]:
                                de_type = st.selectbox('prior type', prior_types,key="de",index=1)
                                de_type += "Prior"
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
                                ho_type += "Prior"
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
                                ho2_type += "Prior"
                            with cols[1]:
                                ho2_mean = st.number_input(label="mean",value=1.0,key="ho2_mean")
                            with cols[2]:
                                ho2_std = st.number_input(label="std",value=0.6,key="ho2_std")
                            with cols[3]:
                                ho2_offset = st.number_input(label="offset",value=0.0,key="ho2_offset")
                                                                                    
                            #op,prm,lwr,upr,men,std,off,mns,shp,scl,tree
                            b1_pr = [de_type,'biallelicBinary.demethylation','','',str(de_mean),str(de_std),str(de_offset),str(de_realSpace),'','','']
                            b2_pr = [ho_type,'biallelicBinary.homozygousMethylation','','',str(ho_mean),str(ho_std),str(ho_offset),str(ho_realSpace),'','','']
                            b3_pr = [ho2_type,'biallelicBinary.homozygousDemethylation','','',str(ho2_mean),str(ho2_std),str(ho2_offset),str(ho2_realSpace),'','','']
                            prrs.update_one_prior(False,'biallelicBinary.demethylation',b1_pr)
                            prrs.update_one_prior(False,'biallelicBinary.homozygousMethylation',b2_pr)
                            prrs.update_one_prior(False,'biallelicBinary.homozygousDemethylation',b3_pr)
                        else:
                            prrs.update_one_prior(True,'biallelicBinary.demethylation',b1_pr)
                            prrs.update_one_prior(True,'biallelicBinary.homozygousMethylation',b2_pr)
                            prrs.update_one_prior(True,'biallelicBinary.homozygousDemethylation',b3_pr)
                    
                                                        
                with st.expander("View or change clock priors"):
                                        
                        clock_priors = st.checkbox("Clock priors",value=False,help="Do you want to set priors on the clock rate?")
                        cl_pr = []
                        if clock_priors:
                            cols = st.columns([1,1,1,1])
                            with cols[0]:
                                prior_type = st.selectbox('prior type', prior_types,key="clock",index=2)
                                prior_type += "Prior"
                            with cols[1]:
                                st.write('clock rate')
                                st.write(clock_rate)
                            with cols[2]:
                                clock_mean = st.number_input(label="clock mean",value=0.0)
                            with cols[3]:
                                clock_std = st.number_input(label="clock std",value=0.1)
                            
                            #op,prm,lwr,upr,men,std,off,mns,shp,scl,tree
                            cl_pr = [prior_type,'clock.rate','','',str(clock_mean),str(clock_std),'','','','','']
                            prrs.update_one_prior(False,'clock.rate',cl_pr)
                        else:
                            prrs.update_one_prior(True,'clock.rate',cl_pr)
                            
                with st.expander("View or change all priors"):
                    edited_pr = st.data_editor(prrs.get_as_dataframe(),num_rows="dynamic",use_container_width=True)
                    prrs.update_from_dataframe(edited_pr)
                
                with st.expander("View or change all operators"):
                    ### OPERATORS #############################################################
                    operators = ops.Operators(demographic,dt_obj.ops)
                    edited_df = st.data_editor(operators.get_as_dataframe(),num_rows="dynamic",use_container_width=True)
                    operators.update_from_dataframe(edited_df)
                                
            ### LOG FILE PARAMS #############################################################
            with tabLog:
                st.write("#### :page_facing_up: Log file params")
                cols = st.columns(2)
                logs = dt_obj.selected_logs(prrs,operators,log_choices)
                logs_all = dt_obj.all_logs(prrs,operators)
                with cols[0]:
                    st.write("Defaults")
                    for k,v in logs.items():
                        include = st.checkbox(k,value=True)
                        if include:
                            if k not in log_choices:
                                log_choices.append(k)
                with cols[1]:
                    st.write("Available")
                    for k in logs_all:
                        if k not in logs:
                            include = st.checkbox(k,value=False)
                            if include:
                                if k not in log_choices:
                                    log_choices.append(k)
                
                
                
            ### GENERATE #############################################################
            with tabGenerate:
                st.write("#### :checkered_flag: Check and save xml")
                ################################################################
                mcmc = mc.MCMC(mcmcs,clocks,prrs,dt_obj,operators,log_choices)
                xmlwriter = xml.XmlWriter(dt_obj,mcmc,lucas,clocks,demographic,dt_obj,operators)
                
                my_xml = xmlwriter.get_xml()
                
                ################################################################
                with st.expander("View generated xml"):
                    #my_xml = st.text_area('Edit xml if necessary, tab out to inactivate box before saving',value=my_xml,height=400)
                    my_xml = st_ace(language="xml", theme="monokai", keybinding="vscode",font_size=12,show_gutter=True,value=my_xml,height=400)
                    
                ################################################################
                #js = widge.get_saveas(my_xml,name)
                #components.html(js, height=30)
                st.download_button("Download xml",data=my_xml,file_name=f"{name}.xml",mime="text/xml")
                                            