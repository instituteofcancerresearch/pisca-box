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
        
def add_widgets():            
    
    tree_out = None
    uploaded_file_ano = None
    uploaded_file = None
                
    st.subheader("Pisca outputs -> tree visualisation")
    tab1,tab2 = st.tabs(["Load annotated tree","Annotate tree"])
    with tab1:
        uploaded_file_ano = st.file_uploader("Select annotated tree file",type=['anotated trees','trees'])                            
        if uploaded_file_ano is not None:            
            tree_out = StringIO(uploaded_file_ano.getvalue().decode("utf-8")).read()
            #print(tree_out)
            with open("out.trees","w") as fw:
                fw.write(tree_out)
          
    with tab2:                        
        uploaded_file = st.file_uploader("Select tree file",type=['trees','trees'])                            
        if uploaded_file is not None:            
            tree_in = StringIO(uploaded_file.getvalue().decode("utf-8")).read()            
            with open("in.trees","w") as fw:
                fw.write(tree_in)
            burnin = st.number_input(label="burnin",value=100)        
            if st.button('run tree-annotation'):
                output = st.empty()            
                with st_capture(output.code):
                    ret  = cmd.run_tree(tree_in,burnin,"out.trees")                    
                    if os.path.isfile("out.trees"):
                        with open("out.trees") as f:
                            tree_out = f.read()                
                                                                                                                      
    if os.path.isfile("out.trees") and (uploaded_file_ano is not None or uploaded_file is not None):
        with st.expander("annotated tree file - expand to view"):
            st.code(tree_out)
        
        try:
            Phylo.convert("out.trees", "nexus", "trees.xml", "phyloxml")
            if os.path.isfile("trees.xml"):
                with open("trees.xml") as f:
                    tree_xml = f.read()                
                with st.expander("phyloxml conversion - expand to view"):
                    st.code(tree_xml)
        except Exception as e:            
            st.error("Error converting to phyloxml, did you give a valid annotated tree file?")
            st.error(str(e))
        
        st.subheader("Plot phylogenetic tree")
        try:
            if st.button('plot tree'):            
                output2 = st.empty()
                tree = Phylo.read("trees.xml", "phyloxml")                    
                #tree = Phylo.read("out.trees", "nexus")
                #st.write(tree.get_terminals())
                #tree.root.color = '#D71AB9'
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
                axes.text(0.5, 0.99, "Phylogenetic tree from pisca-box", horizontalalignment='center', verticalalignment='center', transform=axes.transAxes, fontsize=12)
                st.pyplot(Phylo.draw(tree,axes=axes,show_confidence=True))
        except Exception as e:
            st.error("Error plotting to Bio.Phylo, did you give a valid annotated tree file?")
            st.error(str(e))
            
            

            
            
            #netx = Phylo.to_networkx(tree)
            #print(netx)
            #import networkx as nx
            #from networkx.drawing.nx_pydot import graphviz_layout            
            #pos = graphviz_layout(netx, prog="dot")
            #st.pyplot(nx.draw(netx, pos))
            
                
            #with st_capture(output2.text):                
                #Phylo.draw_ascii(tree)                
                
        
                            
    