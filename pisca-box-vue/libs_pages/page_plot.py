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
        # default all the inputs, some of whch can be implied from the log        
        age,burnin = 60,10
        lucaBranch, hdi_lower,hdi_upper,have_cenancestor,mean_cenancestor = 0,0,0,False,0
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
            with st.expander("Expand consensus tree"):
                st.code(ops_str)
        if os.path.isfile(flog):            
            log_csv = pd.read_csv(flog,sep="\t",header=3)
            with st.expander("Expand log file"):
                st.dataframe(log_csv)
            len_csv = len(log_csv.index)
            if len_csv > 0:
                # Get all the inputs for the script that can be defaulted from the log file
                headers = log_csv.columns                                                                                                                                          
                import statistics
                floor_csv = math.floor(len_csv*burnin/100)                                
                lucaBranch = statistics.mean(log_csv["luca_branch"][floor_csv:])                
                hdi_lower, hdi_upper = az.hdi(log_csv["luca_branch"][floor_csv:].to_numpy(), hdi_prob=0.95)
                if "cenancestorRate" in headers:                                        
                    have_cenancestor = True
                    mean_cenancestor = statistics.mean(log_csv["cenancestorRate"][floor_csv:])                    
                else:
                    have_cenancestor = False
                                            
        st.write("These inputs must be entered")
        cols = st.columns([2,1,1,1])
        with cols[0]:
            title = st.text_input("title","")
        with cols[1]:
            age = st.number_input(label="age",value=age,key="age")
        with cols[2]:
            burnin = st.number_input("burnin(%)",burnin)
            len_csv = len(log_csv.index)                    
        with cols[3]:
            st.write("Use rate")
            have_cenancestor = st.toggle("Use rate",value=have_cenancestor,label_visibility="collapsed")        
            if have_cenancestor:
                use_rate = "Y"
            else:
                use_rate = "N"
                
        st.write("These inputs are defaulted from the (optional) logfile and/or overwritten")
        cols = st.columns(4)
        with cols[0]:
            lucaBranch = st.number_input(label="mean lucaBranch",value=lucaBranch,key="lucaBranchm")        
        with cols[1]:
            hdi_lower = st.number_input(label="lower branch hdp",value=hdi_lower,key="hl")        
        with cols[2]:
            hdi_upper = st.number_input(label="upper branch hdp",value=hdi_upper,key="hu")
        with cols[3]:
            if have_cenancestor:
                mean_cenancestor = st.number_input(label="mean cenAncestor",value=float(mean_cenancestor),key="rt_m",format="%.6f")
                                                    
        if os.path.isfile(outtree):
            if st.button('run r-script'):
                pdf_name = temps.get_pdf_temp(delete=True)
                output = st.empty()
                with cb.st_capture(output.code,temps.get_session_id()):
                    """
                    mccTreeFile=args[1]
                    title=args[2]
                    outputfile=args[3]
                    useRate = args[4]                        
                    age=as.numeric(args[5])
                    # could come from log                    
                    lucaBranch = as.numeric(args[6])
                    lucaRate = as.numeric(args[7])
                    hpdLucaBranch_l = as.numeric(args[8])
                    hpdLucaBranch_u = as.numeric(args[9])
                    """
                    ret = cmd.run_r_script(outtree,title,pdf_name,
                                           use_rate,age,
                                           lucaBranch,mean_cenancestor,
                                           hdi_lower,hdi_upper)
                    print(ret)                
                if os.path.isfile(pdf_name):
                    widgets.show_pdf(pdf_name,height=800)
            
            
                
        
        