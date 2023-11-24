import __init__ # noqa: F401
import libs.cls_dt_biallelic as bb
import libs.cls_dt_acna as ac
import libs.cls_dt_cnv as cv
import libs.cls_dt_phyfum as phy
import pandas as pd
import libs.cls_datadetermine as dd



    
# Choose the fasta and dates file --------------------------------------------------------------------------------------------------
seq = 'C:/dev/beast-icr/pisca-box/pisca-box-vue/tests/fixtures/acna/acna.csv'
ages = 'C:/dev/beast-icr/pisca-box/pisca-box-vue/tests/fixtures/acna/acna_dates.csv'

nm,tp = seq.lower().split(".")
dtd = dd.DataDetermine(None,tp,seq)
dic_seq,dtyp = dtd.get_seq_data()
csv_ages = pd.read_csv(ages)
    
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
    
dic_seq,dtyp = dtd.get_seq_data()
printed = False
for taxon in dic_seq:
    if not printed:
        print(dic_seq[taxon])
        printed = True

print(dtd.seq_data[:20])