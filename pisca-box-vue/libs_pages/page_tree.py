import __init__ # noqa: F401
import streamlit as st
import os
from io import StringIO
from contextlib import contextmanager, redirect_stdout
import libs.cmds as cmd
from Bio import Phylo
from matplotlib import pyplot as plt
import libs.widgets as widgets

#https://dev.to/chrisgreening/complete-list-of-markdown-emojis-for-your-blog-posts-and-readme-s-164j

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
        

def do_plot(internal_tree_file,opts):
    #cmd.run_r_script()
    html_str = ""
    with open("my_plot.svg", "r") as f:
        html_str = f.read()
    st.write(html_str, unsafe_allow_html=True)
    tree = Phylo.read(internal_tree_file, "phyloxml")                                    
    if opts == "Pink":                           
        tree.get_nonterminals()[0].color = '#D71AB9'
        for clade in tree.get_terminals():
            if clade.branch_length < 0.3:
                clade.color = '#A571CC'
            elif clade.branch_length < 0.6:
                clade.color = '#EFA6C6'
            else:
                clade.color = '#D71A6F'                                                            
    tree.ladderize()  # Flip branches so deeper clades are displayed at top            
    st.set_option('deprecation.showPyplotGlobalUse', False)                                
    fig = plt.figure(figsize=(5, 5), dpi=100)
    ax = fig.add_subplot(1, 1, 1)                
    Phylo.draw(tree,axes=ax,show_confidence=True)
    #plt.axvline(0,color="teal",linestyle='--',lw=1)
    ax.set_title("Phylogenetic tree from pisca-box")
    st.pyplot(fig)
    
def remove_internal_files(internal_tree_file_xml,internal_out_file_ano,internal_in_file,internal_tree_file_orig,internal_out_file_orig):    
    if os.path.isfile(internal_tree_file_xml):
        os.remove(internal_tree_file_xml)
    if os.path.isfile(internal_out_file_ano):
        os.remove(internal_out_file_ano)
    if os.path.isfile(internal_in_file):
        os.remove(internal_in_file)
    if os.path.isfile(internal_tree_file_orig):
        os.remove(internal_tree_file_orig)
    if os.path.isfile(internal_out_file_orig):
        os.remove(internal_out_file_orig)
    

def show_b4_plot(file_type,tree_xml,tree_out,tree_in,tree_xml_orig,tree_out_orig):
    
    if file_type == "tree":
        if tree_in is not None:
            st.download_button("Download original trees",tree_in,file_name="original.trees")
            with st.expander("original trees file - expand to view"):
                st.code(tree_in)
        if tree_out_orig is not None:
            st.download_button("Download consensus tree",tree_out_orig,file_name="consensus.tree")
            with st.expander("consensus tree file - expand to view"):
                st.code(tree_out_orig)
        if tree_xml_orig is not None:
            st.download_button("Download original trees",tree_xml_orig,file_name="consensus.xml")
            with st.expander("phyloxml conversion - expand to view"):
                st.code(tree_xml_orig)
    if file_type != "phyloxml" and tree_out is not None :
        with st.expander("annotated tree file - expand to view"):
            st.code(tree_out)                                
    if tree_xml is not None and file_type != "tree":
        with st.expander("phyloxml conversion - expand to view"):
            st.code(tree_xml)


def show_and_plot(file_type,internal_tree_file_xml,internal_out_file_ano,internal_in_file,internal_tree_file_orig,internal_out_file_orig):
    
    tree_xml,tree_out,tree_in,tree_xml_orig,tree_out_orig = None,None,None,None,None
    
    if os.path.isfile(internal_tree_file_xml):
        with open(internal_tree_file_xml) as f:
            tree_xml = f.read()
    if os.path.isfile(internal_out_file_ano):
        with open(internal_out_file_ano) as f:
            tree_out = f.read()                                    
            
    if os.path.isfile(internal_tree_file_orig):
        with open(internal_tree_file_orig) as f:
            tree_xml_orig = f.read()                                    
    if os.path.isfile(internal_out_file_orig):
        with open(internal_out_file_orig) as f:
            tree_out_orig = f.read()        
            
    if os.path.isfile(internal_in_file):
        with open(internal_in_file) as f:
            tree_in = f.read()                            
                                            
    show_b4_plot(file_type,tree_xml,tree_out,tree_in,tree_xml_orig,tree_out_orig)
                    
    if tree_xml is not None:
        st.subheader("Plot phylogenetic tree")
        opts = "Black"#st.radio('Colour scheme:', ["Black", "Pink"],key="clr")                            
        try:
            if st.button('plot tree'):                                                        
                do_plot(internal_tree_file_xml,opts)            
        except Exception as e:
            st.error("Error plotting to Bio.Phylo, did you give a valid annotated tree file?")
            st.error(str(e))
            
        
def add_widgets(include_header,upload_file):
    if include_header:
        widgets.page_header('tree-vue')         
                                                                
    st.subheader("Create consensus tree")
    
    ftree = ""
    outtree = "out.tree"
    if upload_file:
        uploaded_file = st.file_uploader("Upload trees file for consensus",type=['trees','tres'])        
        if uploaded_file is not None:
            string_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            ftree = "upload.trees"
            with open(ftree,"w") as fw:
                fw.write(string_data)
    else:
        if "ftree" in st.session_state:            
            ftree = st.session_state["ftree"]
    if os.path.isfile(ftree):
        with open(ftree) as f:
            tree_str = f.read()
        with st.expander(f"Expand tree file {ftree}"):
            st.code(tree_str)                                             
        burnin = st.number_input(label="burnin",value=10)                    
        if st.button('run tree-annotation'):
            #remove_internal_files(internal_tree_file_orig,internal_out_file_orig,internal_in_file) 
            output = st.empty()            
            with st_capture(output.code):
                cmd.run_tree_from_file(ftree,burnin,outtree)                    
            if os.path.isfile(outtree):
                with open(outtree) as f:
                    tree_out = f.read()
                st.session_state["outtree"] = outtree
                with st.expander("Expand consensus tree"):
                    st.code(tree_out)                                        
                st.download_button("Download consensus tree",tree_out,file_name="consensus.mcc")
            
                                                
# Now load the files again as there can be instatiation erros from embedded buttons
#if uploaded_file is not None:                 
#    show_and_plot(file_type,internal_tree_file_xml,internal_out_file_ano,internal_in_file,internal_tree_file_orig,internal_out_file_orig)
#else:
#    remove_internal_files(internal_tree_file_xml,internal_out_file_ano,internal_in_file,internal_tree_file_orig,internal_out_file_orig)

                                                                                                                    

    