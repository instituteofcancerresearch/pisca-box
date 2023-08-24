import streamlit as st



def add_widgets():   
    st.markdown('Welcome to **pisca-box**.')
    st.markdown("This is a containerised application for pisca-beast, a plug-in to [BEAST](http://beast.community/) (Bayesian Evolutionary Anaylsis Sampling Trees) for cancer research.")
        
    st.markdown("_Application tabs_")
    st.markdown("**pisca-box**: This utility runs a fully working pisca through a container and is primarily intended as an instructional tool")    
    st.markdown("**beauti-box**: Beauti is the java gui application for creating xml files for the beast application. In beauti-box you can create pisca-specific xml files, there is also a brief tutorial on the inputs")
                        
    st.markdown("**pisca-box** is also a [containerised command line image](https://hub.docker.com/r/rachelicr/pisca-box) that can be run locally or on an HPC cluster. This streamlit app is intended for lighter use")
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