import __init__ # noqa: F401
import libs.cls_xml as xml
import libs.cls_phyfum as phyf
import libs.cls_operators as ops
import libs.cls_mcmc as mc

this_dir = "/".join(__file__.split('/')[:-1])


def help_show_dif(stringa, stringb):
    min_len = min(len(stringa),len(stringb))
    for i in range(min_len):
        if stringa[i] != stringb[i]:
            print(i,stringa[i],stringb[i])
            if i > 5 and i < min_len - 5:
                print(i,stringa[i-3:i+3],stringb[i-3:i+3])
                                            
def xtest_phyfum_xml(show_xml=False,save_xml=False,overwrite=False,check_assert = True):
    success = True
         
    trials = []            
    trials.append(['phyf-csv','phyfum/phyfum.csv','phyfum/phyfum.dates.csv','phyf'])
                
    for key,seq_file,seq_ages,seq_type in trials:

        # File selection        
        file_name_data = f'{this_dir}/fixtures/{seq_file}'
        file_name_ages = f'{this_dir}/fixtures/{seq_ages}'                    
        
        # PISCA
        datatype = seq_type #(cnv / acna / bb /phyf)
        
        # load data files into data type
        #if datatype == "phyf":
        fasta = phyf.Phyfum(file_name_data,file_name_ages)
        print(fasta.dic_taxon_seq)
        print(fasta.dic_taxon_age)
                                                
        # CLOCK        
        clock = "strict clock" # ["strict clock", "random local clock"]
        clock_rate = 0.13
        clocks = {}        
        clocks['type'] = clock
        clocks['rate'] = clock_rate
        
        
        # LUCA
        #we want to draw the age
        # 
        # 
        # s from column age and the seq id from column taxon
        min_age,max_age = fasta.get_min_max_ages()
        
        lucas = {}
        lucas["height"] = max_age
        lucas["branch"] = 34
        lucas["lower"] = 0.0
        lucas["upper"] = min_age                
                
        # TREES
        demographic =  "constant size" #["constant size", "exponential growth"]
        
        # MCMC
        mcmcs = {}
        mcmcs['name'] = "my name any"
        mcmcs['chain_length'] = 2500
        mcmcs['log_every'] = 250
        mcmcs['mle'] = True
                
        # PRIORS
        priors = {}
        priors['luca_branch'] = {'prior_type':'uniform','value':max_age}
        priors['clock.rate'] = {'prior_type':'normal','mean':0.0,'std':0.13}
        priors['biallelicBinary.demethylation'] = {'prior_type':'logNormal','mean':1.0,'std':0.6,'offset':0.0,'realSpace':True}
        priors['biallelicBinary.homozygousMethylation'] = {'prior_type':'logNormal','mean':1.0,'std':0.6,'offset':0.0,'realSpace':True}
        priors['biallelicBinary.homozygousDemethylation']= {'prior_type':'logNormal','mean':1.0,'std':0.6,'offset':0.0,'realSpace':True}    
        
                                
        
        #fasta = fa.Fasta(fasta_string,csv_ages,datatype,seq_csv)        
        operators = ops.Operators(demographic,datatype,clocks)
        mcmc = mc.MCMC(mcmcs,clocks,priors)                                    
        xmlwriter = xml.XmlWriter(fasta,mcmc,lucas,clocks,demographic,datatype,operators)

        xmlstr = xmlwriter.get_xml()
        if show_xml:
            print(xmlstr)
        if save_xml:
            filename = f'{this_dir}/fixtures/{seq_file}_fix.xml'
            if not overwrite:
                filename = f'{this_dir}/fixtures/{seq_file}_tst.xml'                
            with open(filename, "w") as f:
                f.write(xmlstr)
                print("saved to",filename)
        xmlstr = xmlstr.replace("\n","").replace(" ","").replace("\t","")
        if check_assert:
            fix_file = f'{this_dir}/fixtures/{seq_file}_fix.xml'
            fix_str = ""
            with open(fix_file, "r") as f:
                fix_str = f.read()
            fix_str = fix_str.replace("\n","").replace(" ","").replace("\t","")
            
            if fix_str != xmlstr:
                help_show_dif(fix_str,xmlstr)
                success = False
            assert fix_str == xmlstr, f"BEAUTI-01 xml strings do not match for {seq_file}"
                            
    return success
            
           
############################################    

#def test_0102():    
#    # these files should be the same
#    trials = []
#    trials.append(['data_01b_patient1.fasta_tst.xml','data_01b_patient1_bb_seq.csv_tst.xml'])
#    
#    for filea,fileb in trials:
#        with open(f'{this_dir}/fixtures/{filea}', "r") as f:
#            filea_str = f.read()
#        filea_str = filea_str.replace("\n","").replace(" ","").replace("\t","")
#                
#        with open(f'{this_dir}/fixtures/{fileb}', "r") as f:
#            fileb_str = f.read()
#        fileb_str = fileb_str.replace("\n","").replace(" ","").replace("\t","")
#        
#        if filea_str != fileb_str:
#            help_show_dif(filea_str,fileb_str)                                                         
#        assert filea_str == fileb_str, f"BEAUTI-02 xml files do not match for {filea} and {fileb}"
    
    
