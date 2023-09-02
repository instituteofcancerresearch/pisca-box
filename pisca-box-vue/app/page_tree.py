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
from contextlib import contextmanager, redirect_stdout, redirect_stderr
import cmds as cmd
from Bio import Phylo
from matplotlib import pyplot as plt

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
    fig = plt.figure(figsize=(10, 20), dpi=100)
    axes = fig.add_subplot(1, 1, 1)    
    #axes.set_title("Phylogenetic tree from pisca-box")
    #axes.text(0.5, 0.99, "Phylogenetic tree from pisca-box", horizontalalignment='center', verticalalignment='center', transform=axes.transAxes, fontsize=12)
    st.pyplot(Phylo.draw(tree,axes=axes,show_confidence=True))
    
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
            with st.expander("original tree file - expand to view"):
                st.code(tree_in)
        if tree_out_orig is not None:
            with st.expander("annotated tree file - expand to view"):
                st.code(tree_out_orig)
        if tree_xml_orig is not None:
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
        opts = st.radio('Colour scheme:', ["Black", "Pink"],key="clr")                            
        try:
            if st.button('plot tree'):                                                        
                do_plot(internal_tree_file_xml,opts)            
        except Exception as e:
            st.error("Error plotting to Bio.Phylo, did you give a valid annotated tree file?")
            st.error(str(e))
    


def add_widgets():            
            
    tree_xml = None
    tree_out = None
    tree_xml_orig = None
    tree_out_orig = None
    tree_in = None        
    uploaded_file = None
    
    internal_tree_file_xml = "trees.xml"
    internal_tree_file_orig = "trees_orig.xml"
    internal_out_file_ano = "out.trees"
    internal_out_file_orig = "out_orig.trees"
    internal_in_file = "in.trees"
                                    
    st.subheader("Pisca outputs -> tree visualisation")
            
    file_type = st.radio("Select tree file type",("phyloxml","annotated","tree"))
    st.divider()
    
    if file_type == "phyloxml":    
        #remove_internal_files(internal_tree_file,internal_out_file,internal_in_file)        
        uploaded_file = st.file_uploader("Upload phloxml tree file",type=['phyloxml tree','xml'])                            
        if uploaded_file is not None:                        
            tree_xml = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            tree_xml = tree_xml.replace("<name>tree1</name>", "<name>pisca-box phylogenetic tree</name>") 
            tree_xml = tree_xml.replace("<name>Tree1</name>", "<name>pisca-box phylogenetic tree</name>") 
            tree_xml = tree_xml.replace("<name>TREE1</name>", "<name>pisca-box phylogenetic tree</name>") 
            with open(internal_tree_file_xml,"w") as fw:
                fw.write(tree_xml)                                                           
    elif file_type == "annotated":
        #remove_internal_files(internal_tree_file,internal_out_file,internal_in_file)        
        uploaded_file = st.file_uploader("Upload annotated tree file",type=['anotated trees','trees'])                            
        if uploaded_file is not None:                            
            tree_out = StringIO(uploaded_file.getvalue().decode("utf-8")).read()            
            with open(internal_out_file_ano,"w") as fw:
                fw.write(tree_out)              
            try:
                Phylo.convert(internal_out_file_ano, "nexus", internal_tree_file_xml, "phyloxml")
                if os.path.isfile(internal_tree_file_xml):
                    with open(internal_tree_file_xml) as f:
                        tree_xml = f.read()
                    tree_xml = tree_xml.replace("<name>tree1</name>", "<name>pisca-box phylogenetic tree</name>") 
                    tree_xml = tree_xml.replace("<name>Tree1</name>", "<name>pisca-box phylogenetic tree</name>") 
                    tree_xml = tree_xml.replace("<name>TREE1</name>", "<name>pisca-box phylogenetic tree</name>") 
                    with open(internal_tree_file_xml,"w") as fw:
                        fw.write(tree_xml)                                                                                               
            except Exception as e:            
                st.error("Error converting to phyloxml, did you give a valid annotated tree file?")
                st.error(str(e))                    
    else:        
        uploaded_file = st.file_uploader("Upload tree file to be annotated",type=['trees','trees'])                            
        if uploaded_file is not None:            
            file_type = "tree"            
            #remove_internal_files(internal_tree_file,internal_out_file,internal_in_file)        
            tree_in = StringIO(uploaded_file.getvalue().decode("utf-8")).read()            
            with open(internal_in_file,"w") as fw:
                fw.write(tree_in)
            burnin = st.number_input(label="burnin",value=100)        
            if st.button('run tree-annotation'):
                #remove_internal_files(internal_tree_file_orig,internal_out_file_orig,internal_in_file) 
                output = st.empty()            
                with st_capture(output.code):
                    ret  = cmd.run_tree(tree_in,burnin,internal_out_file_orig)                    
                if os.path.isfile(internal_out_file_orig):
                    with open(internal_out_file_orig) as f:
                        tree_out = f.read()
                try:
                    Phylo.convert(internal_out_file_orig, "nexus", internal_tree_file_orig, "phyloxml")                    
                    Phylo.convert(internal_out_file_orig, "nexus", internal_tree_file_xml, "phyloxml")
                    if os.path.isfile(internal_tree_file_xml):
                        with open(internal_tree_file_xml) as f:
                            tree_xml = f.read()
                        tree_xml = tree_xml.replace("<name>tree1</name>", "<name>pisca-box phylogenetic tree</name>") 
                        tree_xml = tree_xml.replace("<name>Tree1</name>", "<name>pisca-box phylogenetic tree</name>") 
                        tree_xml = tree_xml.replace("<name>TREE1</name>", "<name>pisca-box phylogenetic tree</name>") 
                        with open(internal_tree_file_xml,"w") as fw:
                            fw.write(tree_xml)                                                                                                                                   
                    if os.path.isfile(internal_tree_file_xml):
                        with open(internal_tree_file_xml) as f:
                            tree_xml_orig = f.read()                                    
                except Exception as e:            
                    st.error("Error converting to phyloxml, did you give a valid annotated tree file?")
                    st.error(str(e))
                
        
                                    
    # Now load the files again as there can be instatiation erros from embedded buttons
    if uploaded_file is not None:         
    #    if os.path.isfile(internal_in_file):
    #        with open(internal_in_file) as f:
    #            tree_in = f.read()                                    
    
        show_and_plot(file_type,internal_tree_file_xml,internal_out_file_ano,internal_in_file,internal_tree_file_orig,internal_out_file_orig)
    else:
        remove_internal_files(internal_tree_file_xml,internal_out_file_ano,internal_in_file,internal_tree_file_orig,internal_out_file_orig)

                                                                                                                      
    
    #if uploaded_file is not None: #phyloxml","annotated","tree
    #    show_and_plot(file_type,tree_xml,tree_out,tree_in,internal_tree_file)
"""                                        
        if file_type == "tree" and tree_in is not None:
            with st.expander("original tree file - expand to view"):
                st.code(tree_in)
        if file_type != "phyloxml" and tree_out is not None :
            with st.expander("annotated tree file - expand to view"):
                st.code(tree_out)                                
        if tree_xml is not None:
            with st.expander("phyloxml conversion - expand to view"):
                st.code(tree_xml)
        
        st.subheader("Plot phylogenetic tree")
        try:
            if st.button('plot tree'):                                            
                do_plot(internal_tree_file)
        except Exception as e:
            st.error("Error plotting to Bio.Phylo, did you give a valid annotated tree file?")
            st.error(str(e))
    
"""         
            

            
            
            #netx = Phylo.to_networkx(tree)
            #print(netx)
            #import networkx as nx
            #from networkx.drawing.nx_pydot import graphviz_layout            
            #pos = graphviz_layout(netx, prog="dot")
            #st.pyplot(nx.draw(netx, pos))
            
                
            #with st_capture(output2.text):                
                #Phylo.draw_ascii(tree)                
                
        
                            
    