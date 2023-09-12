import __init__
import streamlit as st

def add_widgets():                            
    st.markdown('Welcome to **pisca-box-vue**. This application is a user-friendly interface to the pisca-beast plug-in for [BEAST](http://beast.community/) (Bayesian Evolutionary Anaylsis Sampling Trees).')
    st.markdown("The pisca-beast plug-in adapts the BEAST MCMC calculations to apply to cancer evolution. The pisca-beast plug-in was created by Diego Mallo and is available on [github](https://github.com/adamallo/PISCA).")
        
    st.markdown("#### Applications available in pisca-box-vue")
    st.markdown("The BEAST eco-system includes command line utiltities and java gui applications, two of which are exposed here in **pisca-box-vue**")    
    st.markdown("**pisca-box** is the main calculation engine, running the BEAST command-line utility with the PISCA java plug-in.")
    st.markdown("**beauti-box**: beauti is the java gui application for creating xml files for the beast application. In beauti-box you can create pisca-specific xml files, with a helpful guide to the inputs.")
    
    st.markdown("#### Further applications")            
    st.markdown("**pisca-box** is also a [containerised command line image](https://hub.docker.com/r/rachelicr/pisca-box) that can be run locally or on an HPC cluster for heavier-duty use")
    st.markdown("See the help tab for further information on the parameters and inputs for pisca and for the command line version of pisca-box")
    
    st.divider()
    st.write("References:")
    cite1 = """
    Suchard MA, Lemey P, Baele G, Ayres DL, Drummond AJ & Rambaut A (2018)
    Bayesian phylogenetic and phylodynamic data integration using 
    BEAST 1.10 Virus Evolution 4, vey016. DOI:10.1093/ve/vey016
    """    
    st.caption(cite1)
    
    cite2 = """
    Martinez P, Mallo D, Paulson TG, Li X, Sanchez CA, Reid BJ, Graham TA, Kuhner MK and Maley CC (2018) 
    Evolution of Barrett's Esophagus through space and time at single-crypt and whole-biopsy levels. Nat. Commun 9: 794.
    """    
    st.caption(cite2)