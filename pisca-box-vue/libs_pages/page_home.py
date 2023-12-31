import __init__ # noqa: F401
import streamlit as st
import libs.widgets as widgets

def add_widgets(include_header):
    if include_header:
        widgets.page_header('pisca-box')
    st.markdown("""
                
                Welcome to **pisca-box**. This application is a user-friendly interface to the pisca-beast plug-in for
                [BEAST](http://beast.community/) (Bayesian Evolutionary Anaylsis Sampling Trees).
                
                The pisca-beast plug-in adapts the BEAST MCMC calculations to apply to cancer evolution. The pisca-beast plug-in was 
                created by Diego Mallo and is available on [github](https://github.com/adamallo/PISCA).
                                
                The BEAST eco-system includes command line utiltities and java gui applications, two of which are exposed here in **pisca-box**
                
                ---
                
                **beauti-box**: beauti replicates the java gui application for creating xml files for the beast application. 
                In beauti-box you can create pisca-specific xml files, with a helpful guide to the inputs.
                                
                **pisca-box** exposes the main calculation engine, internally running the BEAST command-line utility with the PISCA java plug-in.
                There are some basic tools to view the beast ouputs included:                
                - consensus: the tree annotator tool creates a consensus summary tree from the MCMC trees output. It is is a gui wrapper 
                for the tree annotator command line utility that includes a very basic phylogenetic plot fopr sanity checking purposes.
                - consensus plot: runs a custom R Script to give an indication of the convergence.
                
                ---
                
                #### Further applications
                **pisca-box** is also a [containerised command line image](https://hub.docker.com/r/rachelicr/pisca-run) that can be run locally or on an HPC cluster for heavier-duty use
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
    
                