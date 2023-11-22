import __init__ # noqa: F401
import streamlit as st
import libs_pages.page_beauti as pageBe
import libs_pages.page_pisca as pagePi
import libs_pages.page_tree as pageTv
import libs_pages.page_plot as pageTp

import libs.widgets as widgets
widgets.page_header('plot-box',divider=False)

#https://dev.to/chrisgreening/complete-list-of-markdown-emojis-for-your-blog-posts-and-readme-s-164j

pageTp.add_widgets(False,True)

