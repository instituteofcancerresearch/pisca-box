import __init__ # noqa: F401
import streamlit as st
import libs_pages.page_beauti as pageBe
import libs_pages.page_pisca as pagePi
import libs_pages.page_tree as pageTv

import libs.widgets as widgets
widgets.page_header('pisca-box',divider=False)

#https://dev.to/chrisgreening/complete-list-of-markdown-emojis-for-your-blog-posts-and-readme-s-164j


# Insert containers separated into tabs:
tabBB, tabPB, tabTv  = st.tabs(["beauti-box","pisca-box","tree-vue"])


with tabBB:
    pageBe.add_widgets(False)
with tabPB:
    pagePi.add_widgets(False)
with tabTv:
    pageTv.add_widgets(False)

