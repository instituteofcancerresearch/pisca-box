import libs.cls_datatype as dt
#https://stackoverflow.com/questions/372042/difference-between-abstract-class-and-interface-in-python


class Phyfum(dt.DataType):
    """This is an implementation of DataType. 

    """    
    def __init__(self,seq_data_dic,ages_csv):
        super().__init__(seq_data_dic,ages_csv)               
    ##############################################################
    # ABSTRACT FUNCTIONS TO IMPLEMENT
    ##############################################################                    
    def _get_datatype(self):
        return "cnv"    
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
        return ops
    ##############################################################
    def _default_priors(self):
        prs = []
        prs.append(["exponentialPrior","cnv.loss","","","1.0","","0.0","","","",""])
        #prs.append(["uniformPrior","luca_height","1.0","50","","","","","","",""])
        return prs
    #############################################################
    def _define_default_logs(self):
        defaults = ["posterior","prior","likelihood","coalescent","cenancestorRate"]
        defaults += ["luca_height","luca_branch","clock.rate",".growthRate",".popSize",".changes",".relativeRates",".rootHeight",".loss"]
        return defaults
    #############################################################
    def get_datatype_xml(self):
        gdt = ""
        gdt += '\t<generalDataType id="phyfum">\n'
        gdt += '\t</generalDataType>\n'
        return gdt
    ##############################################################
    def get_site_model(self):
        st = ""
        st += '<siteModel id="siteModel">\n'
        st += '\t<substitutionModel>\n'
        st += '\t\t<PhyfumModel idref="phyfum_subsmodel"/>\n'
        st += '\t</substitutionModel>\n'
        st += '</siteModel>\n'
        return st
    ##############################################################
    def get_character_patterns(self):
        pat = ""        
        state = "H"        
        pat += '<ascertainedCharacterPatterns id="patterns">\n'
        pat += '\t<alignment idref="alignment"/>\n'
        pat += f'\t<state code="{state}"/>\n'
        pat += '</ascertainedCharacterPatterns>\n'
        return pat
    ##############################################################
    def get_frequency_model(self):        
        fm = ""        
        fm += '<frequencyModel id="frequencies">\n'
        fm += f'\t<dataType idref="{self.datatype}"/>\n'
        fm += '\t<frequencies>\n'                
        fm += f'\t\t<parameter id="{self.datatype}.frequencies" value="0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"/>\n'        
        fm += '\t</frequencies>\n'
        fm += '</frequencyModel>\n'	   	  
        return fm
    ##############################################################
    def get_cna_model(self):
        cna = ""    
        cna += '<PhyfumModel id="phyfum_subsmodel">\n'
        cna += '\t<frequencies>\n'
        cna += '\t\t<frequencyModel idref="frequencies"/>\n'
        cna += '\t</frequencies>\n'
        cna += '\t<gain_rate>\n'
        cna += '\t\t<parameter id="cnv.gain" value="1" lower="0"/>\n'
        cna += '\t</gain_rate>\n'
        cna += '\t<loss_rate>\n'
        cna += '\t\t<parameter id="cnv.loss" value="1" lower="0"/>\n'
        cna += '\t</loss_rate>\n'
        cna += '\t<conversion_rate>\n'
        cna += '\t\t<parameter id="cnv.conversion" value="1" lower="0"/>\n'
        cna += '\t</conversion_rate>\n'
        cna += '</PhyfumModel>\n'                      
        return cna    
    ##############################################################
