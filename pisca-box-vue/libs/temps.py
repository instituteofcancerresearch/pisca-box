
import streamlit as st
import os
import datetime
import random

def make_id():
    then = str(datetime.datetime.now())
    rand = random.randint(0,1000000000000)
    nm = f"{then}_{rand}"
    nm = nm.replace(":","_")
    nm = nm.replace(".","_")
    nm = nm.replace(" ","_")
    nm = nm.replace("-","_")
    return nm

def get_today():
    then = str(datetime.datetime.now())[:10]
    then = then.replace(":","_")
    then = then.replace(".","_")
    then = then.replace(" ","_")
    then = then.replace("-","_")    
    return then
        
def get_session_id():
    if "sess_no" not in st.session_state:
        delete_temp_files_from_not_today() # a new session can clean up old files
        st.session_state["sess_no"] = make_id()
    elif str(st.session_state["sess_no"]) == "None":
        st.session_state["sess_no"] = make_id()
    return st.session_state["sess_no"]

def get_pisca_flog():
    return f"pisca_{get_session_id()}.log"
def get_pisca_trees():
    return f"pisca_{get_session_id()}.trees"
def get_pisca_ops():
    return f"pisca_{get_session_id()}.ops"

def get_pisca_temp():
    return f"temp/temp_{get_session_id()}.xml"
def get_outtree_temp():
    return f"temp/upload_{get_session_id()}.mcc"
def get_flog_temp():
    return f"temp/upload_{get_session_id()}.log"
def get_ftree_temp():
    return f"temp/upload_{get_session_id()}.trees"
def get_pdf_temp(delete=False):
    if delete:
        if os.path.isfile(f"temp/plot_{get_session_id()}.pdf"):
            os.remove(f"temp/plot_{get_session_id()}.pdf")
    return f"temp/plot_{get_session_id()}.pdf"

def get_temp_list():
    return [get_pisca_temp(),get_outtree_temp(),get_flog_temp(),get_ftree_temp()]

def get_temp_files():
    # folder path
    dir_path = 'temp/'
    # list to store files
    res = []
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(os.path.join(dir_path, path))
    return res

def delete_temp_files():
    fls = get_temp_files()
    for fl in fls:
        if "make.txt" not in fl:
            os.remove(f"{fl}")
            print(f"{fl} removed")

def delete_temp_files_from_not_today():
    print("perform daily clean")
    tdy = get_today()
    fls = get_temp_files()
    for fl in fls:
        if "make.txt" not in fl:
            if tdy not in fl:
                os.remove(f"{fl}")
                print(f"{fl} removed as not from today")
                
                