import __init__ # noqa: F401
import streamlit as st
import libs.cmds as cmd
import libs.widgets as widgets
from io import StringIO
import pandas as pd
import os
import math
from scipy import optimize
import arviz as az
import libs.temps as temps
import libs.callback as cb


def hdi_scipy(distribution, level=0.95):
	"""
	Get the highest density interval for the distribution, e.g. for a Bayesian posterior, the highest posterior density interval (HPD/HDI)
	"""
	
	# For a given lower limit, we can compute the corresponding 95% interval
	def interval_width(lower):
		upper = distribution.ppf(distribution.cdf(lower) + level)
		return upper - lower
	
	# Find such interval which has the smallest width
	# Use equal-tailed interval as initial guess
	initial_guess = distribution.ppf((1-level)/2)
	optimize_result = optimize.minimize(interval_width, initial_guess)
	
	lower_limit = optimize_result.x[0]
	width = optimize_result.fun
	upper_limit = lower_limit + width
	
	return (lower_limit, upper_limit)

def add_widgets(include_header,upload_file):
    if include_header:
        widgets.page_header('beauti-box')
            
    with st.container():
        output = st.empty()
        age,meen,hdi_lower,hdi_upper,rt,rt_mean,rt_orig_mean,burnin = 60,0,0,0,False,0,0,10
        st.write("#### Plot consensus tree")
        flog,outtree = "",""
        if upload_file:
            uploaded_file = st.file_uploader("Upload consensus tree",type=['tree','mcc'])
            if uploaded_file is not None:
                string_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
                outtree = temps.get_outtree_temp()
                with open(outtree,"w") as fw:
                    fw.write(string_data)
            
            uploaded_log = st.file_uploader("Optionally, upload log",type=['log'])
            if uploaded_log is not None:
                string_log = StringIO(uploaded_log.getvalue().decode("utf-8")).read()
                flog = temps.get_flog_temp()
                with open(flog,"w") as fw:
                    fw.write(string_log)
        else:
            if "flog" in st.session_state:
                flog = st.session_state["flog"]
            if "outtree" in st.session_state:
                outtree = st.session_state["outtree"]
                                
        log_csv = pd.DataFrame()
        if os.path.isfile(outtree):
            with open(outtree) as f:
                ops_str = f.read()
            with st.expander(f"Expand consensus tree"):
                st.code(ops_str)
        if os.path.isfile(flog):
            with open(flog) as f:
                log_str = f.read()
            log_csv = pd.read_csv(flog,sep="\t",header=3)
            with st.expander(f"Expand log file"):
                st.dataframe(log_csv)
                                            
        cols = st.columns([2,1,1])
        with cols[0]:
            title = st.text_input("title","")
        with cols[1]:
            burnin = st.number_input("burnin(%)",burnin)
            len_csv = len(log_csv.index)
            if len_csv > 0:
                floor_csv = math.floor(len_csv*burnin/100)
                headers = log_csv.columns
                # calculate the means and hdi
                #lucaHeight=mean(logData[,luca_height][floor(nrow(logData)*burnin):nrow(logData)])
                #hpdLucaHeight=hdi(logData[,luca_height][floor(nrow(logData)*burnin):nrow(logData)],credMass = 0.95)
                lucas = log_csv["luca_height"][floor_csv:]
                import statistics
                meen = statistics.mean(lucas)
                hdi_lower, hdi_upper = az.hdi(lucas.to_numpy(), hdi_prob=0.95)#hdi_scipy(lucas, level=0.95)
                                                                
                if "cenancestorRate" in headers:
                    #lucaRate=mean(logData[,cenancestorRate][floor(nrow(logData)*burnin):nrow(logData)])
                    rt = True
                    cens = log_csv["cenancestorRate"][floor_csv:]
                    print(cens)
                    rt_orig_mean = statistics.mean(cens)
                    print(rt_orig_mean)
                else:
                    rt = False            
        with cols[2]:
            st.write("Use rate")
            rt = st.toggle("Use rate",value=rt,label_visibility="collapsed")        
            if rt:
                use_rate = "Y"
            else:
                use_rate = "N"
                
        cols = st.columns(5)
        with cols[0]:
            age = st.number_input(label="age",value=age,key="age")
        with cols[1]:
            meen = st.number_input(label="mean",value=meen,key="mean")
        with cols[2]:
            hdi_lower = st.number_input(label="hdi",value=hdi_lower,key="hl")        
        with cols[3]:
            hdi_upper = st.number_input(label="hdi",value=hdi_upper,key="hu")
        with cols[4]:
            if rt:
                rt_mean = st.number_input(label="mean cenAncestor",value=rt_orig_mean,key="rt_m",format="%.6f")
                                                    
        if os.path.isfile(outtree):
            if st.button('run r-script'):
                pdf_name = temps.get_pdf_temp(delete=True)
                output = st.empty()
                with cb.st_capture(output.code,temps.get_session_id()):
                    ret = cmd.run_r_script(outtree,age,meen,hdi_lower,hdi_upper,rt_mean,use_rate,pdf_name,title)
                    print(ret)
                #if os.path.isfile("temp.svg"):
                #    html_str = ""
                #    with open("temp.svg", "r") as f:
                #        html_str = f.read()
                #    st.write(html_str, unsafe_allow_html=True)
                if os.path.isfile(pdf_name):
                    widgets.show_pdf(pdf_name,height=800)
            
            
                
        
        