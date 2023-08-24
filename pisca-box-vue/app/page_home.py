import streamlit as st



def add_widgets():   
    st.markdown('Welcome to **pisca-box**.')
    st.markdown("This is a containerised application for pisca-beast, an adaption of BEAST (Bayesian Evolutionary Anaylsis Sampling Trees) for cancer research.")
    
    
    #st.markdown(":green[$\sqrt{x^2+y^2}=1$] is a Pythagorean identity. :pencil:")
    
    st.divider()
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