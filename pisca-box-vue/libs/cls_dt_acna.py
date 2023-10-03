import libs.cls_datatype as dt

class Acna(dt.DataType):
    """This is an implementation of DataType. 

    """    
    def __init__(self,seq_data_dic,ages_csv):
        super().__init__(seq_data_dic,ages_csv)                 
    ##############################################################
    # ABSTRACT FUNCTIONS TO IMPLEMENT
    ##############################################################                    
    def _get_datatype(self):
        return "acna"        
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
        prs.append(["exponentialPrior","acna.loss","","","1.0","","0.0","","","",""])
        return prs
    ##############################################################
    def get_datatype_xml(self):    
        gdt = ""        
        gdt += "<generalDataType id=\"acna\">" + "\n"
        gdt += "\t<state code=\"@\"/> <!-- Genotype: 0 ; Beast State: 0 -->" + "\n"
        gdt += "\t<state code=\"A\"/> <!-- Genotype: 1 ; Beast State: 1 -->" + "\n"
        gdt += "\t<state code=\"B\"/> <!-- Genotype: 2 ; Beast State: 2 -->" + "\n"
        gdt += "\t<state code=\"C\"/> <!-- Genotype: 3 ; Beast State: 3 -->" + "\n"
        gdt += "\t<state code=\"D\"/> <!-- Genotype: 4 ; Beast State: 4 -->" + "\n"
        gdt += "\t<state code=\"E\"/> <!-- Genotype: 5 ; Beast State: 5 -->" + "\n"
        gdt += "\t<state code=\"F\"/> <!-- Genotype: 6 ; Beast State: 6 -->" + "\n"
        gdt += "\t<state code=\"G\"/> <!-- Genotype: 7 ; Beast State: 7 -->" + "\n"
        gdt += "\t<state code=\"H\"/> <!-- Genotype: 8 ; Beast State: 8 -->" + "\n"
        gdt += "\t<state code=\"I\"/> <!-- Genotype: 9 ; Beast State: 9 -->" + "\n"
        gdt += "\t<state code=\"J\"/> <!-- Genotype: 10 ; Beast State: 10 -->" + "\n"
        gdt += "\t<ambiguity code=\"-\" states=\"@ABCDEFGHIJ\"/>" + "\n"
        gdt += "\t<ambiguity code=\"?\" states=\"@ABCDEFGHIJ\"/>" + "\n"
        gdt += "</generalDataType>" + "\n"        
        return gdt
    ##############################################################
    def get_site_model(self):
        st = ""        
        st += '<siteModel id="siteModel">\n'
        st += '\t<substitutionModel>\n'
        st += '\t\t<AbsoluteCNAModel idref="acna_subsmodel"/>\n'
        st += '\t</substitutionModel>\n'
        st += '</siteModel>\n'        
        return st
    ##############################################################
    def get_character_patterns(self):
        pat = ""                                
        state = "B"            
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
        fm += f'\t\t<parameter id="{self.datatype}.frequencies" value="0 0 1 0 0 0 0 0 0 0 0"/>\n'        
        fm += '\t</frequencies>\n'
        fm += '</frequencyModel>\n'	   	  
        return fm
    ##############################################################
    def get_cna_model(self):
        cna = ""        
        cna += '<AbsoluteCNAModel id="acna_subsmodel">\n'
        cna += '\t<frequencies>\n'
        cna += '\t\t<frequencyModel idref="frequencies"/>\n'
        cna += '\t</frequencies>\n'
        cna += '\t<gain_rate>\n'
        cna += '\t\t<parameter id="acna.gain" value="1" lower="0"/>\n'
        cna += '\t</gain_rate>\n'
        cna += '\t<relative_loss_rate>\n'
        cna += '\t\t<parameter id="acna.loss" value="1" lower="0"/>\n'
        cna += '\t</relative_loss_rate>\n'
        cna += '</AbsoluteCNAModel>\n'        
        return cna