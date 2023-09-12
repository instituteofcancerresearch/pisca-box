import streamlit as st
import os
from io import StringIO
from contextlib import contextmanager, redirect_stdout
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
        

def do_plot(tree):
    st.set_option('deprecation.showPyplotGlobalUse', False)                                
    fig = plt.figure(figsize=(10, 20), dpi=100)
    axes = fig.add_subplot(1, 1, 1)    
    #axes.set_title("Phylogenetic tree from pisca-box")
    axes.text(0.5, 0.99, "Phylogenetic tree from pisca-box", horizontalalignment='center', verticalalignment='center', transform=axes.transAxes, fontsize=12)
    st.pyplot(Phylo.draw(tree,axes=axes,show_confidence=True))


def add_widgets():            
    
    tree_out = None
    tree_in = None
    #uploaded_file_ano = None
    #uploaded_file = None
    tree_xml = None
                
    st.subheader("Pisca outputs -> tree visualisation")
    tab1,tab2,tab3 = st.tabs(["Load phyloxml tree","Load annotated tree","Annotate tree"])
        
    with tab1:
        uploaded_file_xml = st.file_uploader("Select phloxml tree file",type=['phyloxml tree','xml'])                            
        if uploaded_file_xml is not None:            
            tree_xml = StringIO(uploaded_file_xml.getvalue().decode("utf-8")).read()                
    with tab2:
        uploaded_file_ano = st.file_uploader("Select annotated tree file",type=['anotated trees','trees'])                            
        if uploaded_file_ano is not None:            
            tree_out = StringIO(uploaded_file_ano.getvalue().decode("utf-8")).read()            
            with open("out.trees","w") as fw:
                fw.write(tree_out)          
    with tab3:                        
        uploaded_file = st.file_uploader("Select tree file",type=['trees','trees'])                            
        if uploaded_file is not None:            
            tree_in = StringIO(uploaded_file.getvalue().decode("utf-8")).read()            
            with open("in.trees","w") as fw:
                fw.write(tree_in)
            burnin = st.number_input(label="burnin",value=100)        
            if st.button('run tree-annotation'):
                output = st.empty()            
                with st_capture(output.code):
                    cmd.run_tree(tree_in,burnin,"out.trees")                    
                    if os.path.isfile("out.trees"):
                        with open("out.trees") as f:
                            tree_out = f.read()                
                                                                                                                      
    st.divider()
    #if os.path.isfile("out.trees") and (uploaded_file_ano is not None or uploaded_file is not None):
    if tree_in is not None:
        with st.expander("original tree file - expand to view"):
            st.code(tree_in)
            
    if tree_out is not None:
        with st.expander("annotated tree file - expand to view"):
            st.code(tree_out)
        
        try:
            Phylo.convert("out.trees", "nexus", "trees.xml", "phyloxml")
            if os.path.isfile("trees.xml"):
                with open("trees.xml") as f:
                    tree_xml = f.read()                                
        except Exception as e:            
            st.error("Error converting to phyloxml, did you give a valid annotated tree file?")
            st.error(str(e))
        
    if tree_xml is not None and os.path.isfile("trees.xml"):
        opts = st.radio('Colour scheme:', ["Black", "Pink"],key="clr")       
                                            
        with st.expander("phyloxml - expand to view"):
            st.code(tree_xml)
        st.write("Options for visualisation")
        
        st.divider()
        st.subheader("Plot of phylogenetic tree")
                                    
        # set up tree
        tree = Phylo.read("trees.xml", "phyloxml") 
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
        
        do_plot(tree)
                                                                                      
                
        
                            
    