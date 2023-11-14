import libs.cls_datatype as dt

class Biallelic(dt.DataType):
    """This is an implementation of DataType. 

    """    
    def __init__(self,seq_data_dic,ages_csv):
        super().__init__(seq_data_dic,ages_csv)                
    ##############################################################
    # ABSTRACT FUNCTIONS TO IMPLEMENT
    ##############################################################                    
    def _get_datatype(self):
        return "biallelicBinary"        
    ##############################################################                                
    def _load_data(self):
        raise self._load_ages_data()
    ##############################################################
    def _default_operators(self):
        ops = []        
        # operator, paramater, weight, scaleFactor, size, gaussian        
        ops.append(['scaleOperator','clock.rate','10.0','0.5','',''])
        ops.append(['subtreeSlide','treeModel','15.0','','2.5','true'])
        ops.append(['narrowExchange','treeModel','15.0','','',''])
        ops.append(['wideExchange','treeModel','3.0','','',''])
        ops.append(['wilsonBalding','treeModel','3.0','','',''])
        ops.append(['scaleOperator','treeModel.rootHeight','5.0','0.75','',''])
        ops.append(['uniformOperator','treeModel.internalNodeHeights','30.0','','',''])
        ops.append(['scaleOperator','luca_branch','1.0','0.2','',''])        
        ops.append(['upDownOperator',  'clock.rate|treeModel.allInternalNodeHeights','5.0','0.75','',''])                
        ops.append(['scaleOperator','biallelicBinary.demethylation','0.25','0.25','',''])
        ops.append(['scaleOperator','biallelicBinary.homozygousMethylation','0.25','0.25','',''])
        ops.append(['scaleOperator','biallelicBinary.homozygousDemethylation','0.25','0.25','',''])
        return ops
    ##############################################################                    
    def _default_priors(self):
        prs = []
        prs.append(["logNormalPrior","biallelicBinary.demethylation","","","1.0","0.6","0.0","true","","",""])
        prs.append(["logNormalPrior","biallelicBinary.homozygousMethylation","","","1.0","0.6","0.0","true","","",""])
        prs.append(["logNormalPrior","biallelicBinary.homozygousDemethylation","","","1.0","0.6","0.0","true","","",""])
        #prs.append(["uniformPrior","luca_height","1.0","50","","","","","","",""])
        return prs    
    #############################################################
    def _define_default_logs(self):
        defaults = ["posterior","prior","likelihood","coalescent","rateChanges","coefficientOfVariation","covariance","cenancestorRate"]
        defaults += ["luca_height","luca_branch","clock.rate",".growthRate",".popSize",".changes",".relativeRates",".rootHeight",".loss"]
        return defaults        
    #############################################################
    def get_datatype_xml(self):    
        gdt = ""
        gdt += '<generalDataType id="biallelicBinary">\n'
        gdt += '<state code="0"/> <!-- Genotype: 0 ; Beast State: 0 -->\n'
        gdt += '<state code="1"/> <!-- Genotype: 1 ; Beast State: 1 -->\n'
        gdt += '<state code="2"/> <!-- Genotype: 2 ; Beast State: 2 -->\n'
        gdt += '</generalDataType>\n' 
        return gdt
    ##############################################################
    def get_site_model(self):
        st = ""        
        st += '<siteModel id="siteModel">\n'
        st += '\t<substitutionModel>\n'
        st += '\t\t<BiallelicBinaryModel idref="biallelicBinary_subsmodel"/>\n'
        st += '\t</substitutionModel>\n'
        st += '</siteModel>\n'            
        return st
    ##############################################################
    def get_character_patterns(self):
        pat = ""        
        pat += '<patterns id="patterns" from="1">\n'
        pat += '\t<alignment idref="alignment"/>\n'
        pat += '</patterns>\n'        
        return pat
    ##############################################################
    def get_frequency_model(self):        
        fm = ""        
        fm += '<frequencyModel id="frequencies">\n'
        fm += f'\t<dataType idref="{self.datatype}"/>\n'
        fm += '\t<frequencies>\n'        
        fm += f'\t\t<parameter id="{self.datatype}.frequencies" value="0.5 0 0.5"/>\n'
        fm += '\t</frequencies>\n'
        fm += '</frequencyModel>\n'	   	  
        return fm
    ##############################################################
    def get_cna_model(self):
        cna = ""                        
        cna += '<BiallelicBinaryModel id="biallelicBinary_subsmodel">\n'
        cna += '\t<frequencies>\n'
        cna += '\t\t<frequencyModel idref="frequencies"/>\n'
        cna += '\t</frequencies>\n'                        
        cna += '\t<demethylation_rate>\n'
        cna += '\t\t<parameter id="biallelicBinary.demethylation" value="1" lower="0"/>\n'
        cna += '\t</demethylation_rate>\n'
        cna += '\t<homozygousDemethylation_rate>\n'
        cna += '\t\t<parameter id="biallelicBinary.homozygousDemethylation" value="1" lower="0"/>\n'
        cna += '\t</homozygousDemethylation_rate>\n'
        cna += '\t<homozygousMethylation_rate>\n'
        cna += '\t\t<parameter id="biallelicBinary.homozygousMethylation" value="1" lower="0"/>\n'
        cna += '\t</homozygousMethylation_rate>\n'                    
        cna += '</BiallelicBinaryModel>\n'            
        return cna    
    ##############################################################
    