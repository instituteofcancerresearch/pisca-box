# ruff: noqa: F841
import __init__ # noqa: F401
import libs.cls_xml as xml
import libs.cls_dt_biallelic as bb
import libs.cls_dt_acna as ac
import libs.cls_dt_cnv as cv
import libs.cls_dt_phyfum as phy
import libs.cls_operators as ops
import libs.cls_mcmc as mc
import pandas as pd
import libs.cls_priors as prs
import libs.cls_datadetermine as dd
"""

This script tests the screen for beauti
"""

# Choose the fasta and dates file --------------------------------------------------------------------------------------------------
seq = '/home/ralcraft/dev/beast-icr/pisca-box/pisca-box-vue/tests/fixtures/biallelic/patient1_seq.csv'
ages = '/home/ralcraft/dev/beast-icr/pisca-box/pisca-box-vue/tests/fixtures/biallelic/patient1_ages.csv'

nm,tp = seq.lower().split(".")
dtd = dd.DataDetermine(None,tp,seq)
dic_seq,dtyp = dtd.get_seq_data()                
csv_ages = pd.read_csv(ages)

# Choose the pisca settings --------------------------------------------------------------------------------------------------
# it should have default automatically
print("The inferred pisca type is: ", dtd.datatype)
if dtyp == 'biallelic':
    dt_obj =  bb.Biallelic(dic_seq,csv_ages)
elif dtyp == 'acna':
    dt_obj =  ac.Acna(dic_seq,csv_ages)
elif dtyp == "cnv":
    dt_obj =  cv.Cnv(dic_seq,csv_ages)
elif dtyp == "phyfum":
    dt_obj =  phy.Phyfum(dic_seq,csv_ages)
else:
    print("Unrecognised datatype",dtyp)

# Choose the clock settings --------------------------------------------------------------------------------------------------
#clock = "strict clock"
clock = "random local clock"
clock_rate = 0.13
clocks = {}        
clocks['type'] = clock
clocks['rate'] = clock_rate

# Choose the luca settings --------------------------------------------------------------------------------------------------
max_age = csv_ages['age'].max()   
min_age = csv_ages['age'].min()
lucas = {}
lucas["height"] = max_age
lucas["branch"] = int((max_age - min_age) / 2)
lucas["lower"] = 0.0
lucas["upper"] = min_age                

# Choose the mcmc settings --------------------------------------------------------------------------------------------------
#demographic =  "constant size"
demographic =  "exponential growth"
mcmcs = {}
mcmcs['name'] = "my name any"
mcmcs['chain_length'] = 1000
mcmcs['log_every'] = 10
mcmcs['mle'] = False
        

# Choose the priors and operators and logs --------------------------------------------------------------------------------------------------
operators = ops.Operators(demographic,dt_obj.ops)
prrs = prs.Priors(demographic,dt_obj.prs)

logs = dt_obj.selected_logs(prrs,operators,[])
print(dt_obj.selected_logs(prrs,operators))
logs_all = dt_obj.all_logs(prrs,operators)                
choices = []
for log,p in logs.items():
    if log not in choices:
        choices.append(log)


# Create the mcmc and xml objects --------------------------------------------------------------------------------------------------
mcmc = mc.MCMC(mcmcs,clocks,prrs,dt_obj,operators,choices)
xmlwriter = xml.XmlWriter(dt_obj,mcmc,lucas,clocks,demographic,dt_obj,operators)                                        

# Generate the xml file --------------------------------------------------------------------------------------------------        
xmlstr = xmlwriter.get_xml()
#print(xmlstr)



