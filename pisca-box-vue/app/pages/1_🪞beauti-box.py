import __init__ # noqa: F401
import streamlit as st
import libs_pages.page_beauti as pageBe
import libs_pages.page_pisca as pagePi
import libs_pages.page_tree as pageTv
import libs_pages.page_plot as pageTp

import libs.widgets as widgets
widgets.page_header('beauti-box',divider=False,other_icon="mirror")

#https://dev.to/chrisgreening/complete-list-of-markdown-emojis-for-your-blog-posts-and-readme-s-164j

pageBe.add_widgets(False)


