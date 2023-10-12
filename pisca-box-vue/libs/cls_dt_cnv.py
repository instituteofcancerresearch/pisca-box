import libs.cls_datatype as dt
#https://stackoverflow.com/questions/372042/difference-between-abstract-class-and-interface-in-python


class Cnv(dt.DataType):
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
        prs.append(["uniformPrior","luca_height","1.0","50","","","","","","",""])
        return prs
    #############################################################
    def _define_default_logs(self):
        defaults = ["posterior","prior","likelihood","coalescent","rateChanges","coefficientOfVariation","covariance","cenancestorRate"]
        defaults += ["luca_height","luca_branch","clock.rate",".growthRate",".popSize",".changes",".relativeRates",".rootHeight",".loss"]
        return defaults    
    #############################################################        
    def get_datatype_xml(self):        
        gdt = ""        
        gdt += '\t<generalDataType id="cnv">\n'
        gdt += '\t<state code="@"/> <!-- Genotype: 0,0 ; Beast State: 0 -->\n'
        gdt += '\t<state code="A"/> <!-- Genotype: 0,1 ; Beast State: 1 -->\n'
        gdt += '\t<state code="B"/> <!-- Genotype: 0,2 ; Beast State: 2 -->\n'
        gdt += '\t<state code="C"/> <!-- Genotype: 0,3 ; Beast State: 3 -->\n'
        gdt += '\t<state code="D"/> <!-- Genotype: 0,4 ; Beast State: 4 -->\n'
        gdt += '\t<state code="E"/> <!-- Genotype: 0,5 ; Beast State: 5 -->\n'
        gdt += '\t<state code="F"/> <!-- Genotype: 0,6 ; Beast State: 6 -->\n'
        gdt += '\t<state code="G"/> <!-- Genotype: 1,0 ; Beast State: 7 -->\n'
        gdt += '\t<state code="H"/> <!-- Genotype: 1,1 ; Beast State: 8 -->\n'
        gdt += '\t<state code="I"/> <!-- Genotype: 1,2 ; Beast State: 9 -->\n'
        gdt += '\t<state code="J"/> <!-- Genotype: 1,3 ; Beast State: 10 -->\n'
        gdt += '\t<state code="K"/> <!-- Genotype: 1,4 ; Beast State: 11 -->\n'
        gdt += '\t<state code="L"/> <!-- Genotype: 1,5 ; Beast State: 12 -->\n'
        gdt += '\t<state code="M"/> <!-- Genotype: 2,0 ; Beast State: 13 -->\n'
        gdt += '\t<state code="N"/> <!-- Genotype: 2,1 ; Beast State: 14 -->\n'
        gdt += '\t<state code="O"/> <!-- Genotype: 2,2 ; Beast State: 15 -->\n'
        gdt += '\t<state code="P"/> <!-- Genotype: 2,3 ; Beast State: 16 -->\n'
        gdt += '\t<state code="Q"/> <!-- Genotype: 2,4 ; Beast State: 17 -->\n'
        gdt += '\t<state code="R"/> <!-- Genotype: 3,0 ; Beast State: 18 -->\n'
        gdt += '\t<state code="S"/> <!-- Genotype: 3,1 ; Beast State: 19 -->\n'
        gdt += '\t<state code="T"/> <!-- Genotype: 3,2 ; Beast State: 20 -->\n'
        gdt += '\t<state code="U"/> <!-- Genotype: 3,3 ; Beast State: 21 -->\n'
        gdt += '\t<state code="V"/> <!-- Genotype: 4,0 ; Beast State: 22 -->\n'
        gdt += '\t<state code="W"/> <!-- Genotype: 4,1 ; Beast State: 23 -->\n'
        gdt += '\t<state code="X"/> <!-- Genotype: 4,2 ; Beast State: 24 -->\n'
        gdt += '\t<state code="Y"/> <!-- Genotype: 5,0 ; Beast State: 25 -->\n'
        gdt += '\t<state code="Z"/> <!-- Genotype: 5,1 ; Beast State: 26 -->\n'
        gdt += '\t<state code="["/> <!-- Genotype: 6,0 ; Beast State: 27 -->\n'
        gdt += '\t<ambiguity code="-" states="@ABCDEFGHIJKLMNOPQRSTUVWXYZ["/>\n'
        gdt += '\t<ambiguity code="?" states="@ABCDEFGHIJKLMNOPQRSTUVWXYZ["/>\n'
        gdt += '\t</generalDataType>\n'        
        return gdt
    ##############################################################
    def get_site_model(self):
        st = ""        
        st += '<siteModel id="siteModel">\n'
        st += '\t<substitutionModel>\n'
        st += '\t\t<CNVModel idref="cnv_subsmodel"/>\n'
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
        cna += '<CNVModel id="cnv_subsmodel">\n'
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
        cna += '</CNVModel>\n'                      
        return cna    
    ##############################################################
