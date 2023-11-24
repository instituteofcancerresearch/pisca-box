import __init__ # noqa: F401
import streamlit as st
from PIL import Image
import libs.widgets as widgets


def add_widgets(include_header):       
    if include_header:
        widgets.page_header('About pisca-box')
    image = Image.open('app/static/icr.png')
    st.markdown("""
                
               [PISCA](https://github.com/adamallo/PISCA)(Phylogenetic Inference using Somatic Chromosomal Alterations) created by Diego Mallo and originally introduced in Martinez et al., 2018, is a Bayesian phylogenetics tool for the modelling of tumour evolution using mutli-region somatic chromosomal alterations (SCA) data. 
               SCA data can take the form of allele specific copy number from deep genome or SNP arrays (i.e. which chromosomes paternal /maternal have been amplified) or absolute copy number (i.e. total copy number, agnostic to which chromosomes). 
               
               [BEAST](http://beast.community/) is a large Bayesian phylogenetic project, which is used for species and pathogen evolution. It produces rooted, time-calibrated trees with a rich array of models including clocks (strict, relaxed) and demographics (constant or exponentially growing populations). 
               The most common datatype is DNA sequences, although it can also has codon and binary models. There are two BEAST projects, BEAST1 and BEAST2 with an overlapping core framework but some differences in specific models available. 
               
               PISCA extends the classic BEAST (1.8.4) framework for the use in somatic evolution. Unlike in species evolution, the ancestor is known to be a diploid, healthy cell.
               An important modification therefore includes the last common ancestor with an unaltered genomic state (LUCA) as a branch from the 'root' of the tree to the most recent common ancestor (MRCA) of the samples.
               Another important modification is the use of SCA substitution models with gains, losses (and LOH for allele-specific).
               
               [pisca-box](https://github.com/rachelicr/pisca-box) was created by Rachel Alcraft and Heather Grant with support from Diego Mallo. This containerized version bypasses the more involved installation steps and dependency clashes. 
               Like BEAST, PISCA also requires the creation of XML files to start analysis, which can be done in PISCA-box and tested out to check for errors. 
               
                
                """)
    st.divider()
    st.markdown("""
                
                #### Collaborators
                **Arizona State University**  
                [Diego Mallo](mailto:dmalload@asu.edu), postdoctoral researcher in the Biodesign Institute
                          
             """)                         
    
    st.image(image)
    st.markdown('<span style="color:yellowgreen">Institute</span><span style="color:orange"> of</span><span style="color:hotpink"> Cancer</span><span style="color:darkred"> Research</span>', unsafe_allow_html=True)        
    
    st.markdown("""
                
                [Heather Grant](mailto:heather.grant@icr.ac.uk), postdoctoral researcher in GEDy lab  
                [Rachel Alcraft](mailto:rachel.alcraft@icr.ac.uk), research software engineer in Scientific Computing
                
                """)
    
    
    
    
    