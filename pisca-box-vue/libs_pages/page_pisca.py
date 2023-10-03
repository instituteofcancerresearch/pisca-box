import __init__ # noqa: F401
import streamlit as st
import os
from contextlib import contextmanager, redirect_stdout
from io import StringIO
#import cmds_tst as cmd
import libs.widgets as widge
import libs.cmds as cmd
import pandas as pd
import streamlit.components.v1 as components
import libs.widgets as widgets

IS_TEST = False

@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret
        
        stdout.write = new_write
        yield
    
######################################################################
def add_widgets(include_header):
    if include_header:
        widgets.page_header('pisca-box')
        
    st.subheader("Choose an xml file")
    uploaded_file = st.file_uploader("upload xml file",type=['xml'])                            
    if uploaded_file is not None:                                
        string_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        full_file_name = "temp.xml"
        with open(full_file_name,"w") as fw:
            fw.write(string_data)
                                                        
        
        if os.path.isfile(full_file_name):
        
            st.subheader("Input parameters")
            col1,col2 = st.columns(2)
            with col1:
                params_input = st.text_input("Enter additional beast parameters",value="-beagle_off")
            #with col2:
            #    burnin = st.number_input(label="Enter annotation burnin",value=100)
            st.subheader("Check inputs and run")
            if st.button('run pisca-box'):                        
                output = st.empty()
                params = []
                if params_input != "":
                    params = params + params_input.split(" ")
                    for pm in params:
                        if pm not in params and len(pm) > 2:
                            params.append(pm)
                params2 = ["-working", "-overwrite",full_file_name]                
                for pm in params2:
                    if pm not in params and len(pm) > 2:
                        params.append(pm)
                ret = ""
                
                with st_capture(output.code):
                    ret  = cmd.run_beast(params)
                    #str = cmd.run_validation(["/project","/project/xml","/mnt"])
                    #print(str)                    
                    if ret == "done":
                        ops_str,tree_str,log_str = "","",""
                        flog = cmd.get_logs(string_data,".log")
                        fops = cmd.get_logs(string_data,".ops")
                        ftree = cmd.get_logs(string_data,".trees")
                        #fmle = False
                                                                        
                        log_csv = pd.DataFrame()
                        if os.path.isfile(fops):
                            with open(fops) as f:
                                ops_str = f.read()
                        if os.path.isfile(ftree):
                            with open(ftree) as f:
                                tree_str = f.read()
                        if os.path.isfile(flog):
                            with open(flog) as f:
                                log_str = f.read()
                            log_csv = pd.read_csv(flog,sep="\t",header=3)
                            
                        #nm,ext = flog.split(".")
                        #if os.path.isfile(f"{nm}.mle.log"):
                        #    fmle = True
                        #    with open(f"{nm}.mle.log") as f:
                        #        log_mle = f.read()
                        
                        
                        #nm,ext = ftree.split(".")
                        #fano = nm + "_annotated." + ext
                        #fxml = nm + "_anno_tree.xml"
                        #ret  = cmd.run_tree(tree_str,burnin,fano)
                        #if os.path.isfile(fano):
                        #    with open(fano) as f:
                        #        ano_str = f.read()
                                                                
                
                
                        st.divider()
                        st.write("Save output logs")
                        nm,ext = fops.split(".")
                        col1,col2 = st.columns([5,1])
                        with col1:                
                            with st.expander(f"expand {fops}"):                                        
                                st.code(ops_str)                
                        with col2:
                            js = widge.get_saveas(ops_str,nm,ext,"Save ops")
                            components.html(js, height=30)                                                                            
                        
                        nm,ext = flog.split(".")
                        col1,col2 = st.columns([5,1])
                        with col1:                
                            with st.expander(f"expand {flog}"):
                                st.write(log_csv)
                        with col2:
                            js = widge.get_saveas(log_str,nm,ext,"Save log")
                            components.html(js, height=30)   
                                                        
                        #if fmle:
                        #    col1,col2 = st.columns([5,1])
                        #    with col1:                
                        #        with st.expander(f"expand {nm}.mle.log"):
                        #            st.write(log_mle)
                        #    with col2:
                        #        js = widge.get_saveas(log_mle,f"{nm}.mle","log","Save mle log")
                        #        components.html(js, height=30)   
                            
                        nm,ext = ftree.split(".")
                        col1,col2 = st.columns([5,1])
                        with col1:                
                            with st.expander(f"expand {ftree}"):
                                st.code(tree_str)
                        with col2:
                            js = widge.get_saveas(tree_str,nm,ext,"Save trees")
                            components.html(js, height=30)   
                    else:
                        st.error("The BEAST application failed") 
                
                    
                                                
                
                """
                st.divider()
                st.write("Save output trees")
                col3,col4,col5 = st.columns(3)                
                
                                        
                with col4:        
                    nm,ext = fano.split(".")
                    js = widge.get_saveas(ano_str,nm,ext,"Save annotated tree")
                    components.html(js, height=30)   
                    with st.expander(f"expand {fano}"):
                        st.code(ano_str)
                        
                with col5:
                    try:
                        Phylo.convert(fano, "nexus", fxml, "phyloxml")
                        if os.path.isfile(fxml):
                            with open(fxml) as f:
                                tree_xml = f.read()
                            nm,ext = fxml.split(".")
                            js = widge.get_saveas(tree_xml,nm,ext,"Save phyloxml")
                            components.html(js, height=30)                                                                            
                            with st.expander(f"expand {fxml}"):
                                st.code(tree_xml)
                    except Exception as e:            
                        st.error("Error converting to phyloxml, did you give a valid annotated tree file?")
                        st.error(str(e))
                                                                    
        else:
            st.error(f"{full_file_name} is not a valid file, please check the working directory")
            result = subprocess.run(["ls","-l"],stdout=subprocess.PIPE)
            if result:
                st.error("These are the available files:")
                st.error(result.stdout.decode('utf-8'))
            """