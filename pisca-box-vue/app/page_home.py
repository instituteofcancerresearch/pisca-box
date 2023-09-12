import __init__ # noqa: F401
import streamlit as st

def add_widgets():                            
    st.markdown("""
                
                Welcome to **pisca-box-vue**. This application is a user-friendly interface to the pisca-beast plug-in for
                [BEAST](http://beast.community/) (Bayesian Evolutionary Anaylsis Sampling Trees).
                
                The pisca-beast plug-in adapts the BEAST MCMC calculations to apply to cancer evolution. The pisca-beast plug-in was 
                created by Diego Mallo and is available on [github](https://github.com/adamallo/PISCA).
                                
                The BEAST eco-system includes command line utiltities and java gui applications, two of which are exposed here in **pisca-box-vue**
                
                1. **pisca-box** is the main calculation engine, running the BEAST command-line utility with the PISCA java plug-in.
                2. **beauti-box**: beauti is the java gui application for creating xml files for the beast application. 
                In beauti-box you can create pisca-specific xml files, with a helpful guide to the inputs.
                3. **tree-vue**: the tree annotator tool creates a consensus summary tree from the MCMC trees output. 
                tree-vue is a gui wrapper for the tree annotator command line utility that includes a very basic phylogenetic plot fopr sanity checking purposes.
                
                
                #### Further applications
                **pisca-box** is also a [containerised command line image](https://hub.docker.com/r/rachelicr/pisca-box) that can be run locally or on an HPC cluster for heavier-duty use
                See the help tab for further information on the parameters and inputs for pisca and for the command line version of pisca-box
                
                """)
    
                            
    st.divider()
    st.write("References:")    
    st.caption("""
                
                Suchard MA, Lemey P, Baele G, Ayres DL, Drummond AJ & Rambaut A (2018)
                Bayesian phylogenetic and phylodynamic data integration using 
                BEAST 1.10 Virus Evolution 4, vey016. DOI:10.1093/ve/vey016
                
                Martinez P, Mallo D, Paulson TG, Li X, Sanchez CA, Reid BJ, Graham TA, Kuhner MK and Maley CC (2018) 
                Evolution of Barrett's Esophagus through space and time at single-crypt and whole-biopsy levels. Nat. Commun 9: 794.
                
                """)
    
                