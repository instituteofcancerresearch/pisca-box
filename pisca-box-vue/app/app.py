import streamlit as st
import page_beauti as pageBe
import page_about as pageAb
import page_home as pageHm
import page_help as pageHe
import page_pisca as pagePi
import page_tree as pageTv

st.set_page_config(page_title='pisca-vue', page_icon = None, 
                   layout = 'wide', initial_sidebar_state = 'auto')
# favicon being an object of the same kind as the one you should provide st.image() with (ie. a PIL array for example) or a string (url or local file path)
st.title(':gift: Pisca-Box-Vue')

# Insert containers separated into tabs:
tabHm, tabBB, tabPB, tabTv, tabHlp, tabAb = st.tabs(["home","beauti-box","pisca-box","tree-vue","help","about"])

with tabHm:
    pageHm.add_widgets()    
with tabBB:
    pageBe.add_widgets()    
with tabPB:
    pagePi.add_widgets()        
with tabTv:
    pageTv.add_widgets()        
with tabHlp:
    pageHe.add_widgets()    
with tabAb:
    pageAb.add_widgets()

#with tabTs:
#    pageTs.add_widgets()
    