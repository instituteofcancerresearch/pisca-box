
# ruff: noqa: E501

class Priors(object):
    def __init__(self,demographic,datatype,clocks):
        self.datatype = datatype
        self.datatype = demographic
        self.clocks = clocks
        self.priors = {}
        
        self.priors["luca_branch"] = ["uniformPrior","73"]
        self.priors["luca_height"] = ["uniformPrior","50"]
        self.priors['biallelicBinary.demethylation'] = ['logNormalPrior','1.0','0.6','0.0','realSpace']
        self.priors['biallelicBinary.homozygousMethylation'] = ['logNormalPrior','1.0','0.6','0.0','realSpace']
        self.priors['biallelicBinary.homozygousDemethylation']= ['logNormalPrior','1.0','0.6','0.0','realSpace']
        
        self.ops.append(['scaleOperator','clock.rate','0.5','10.0'])
        self.ops.append(['subtreeSlide','treeModel','2.5','true','15.0'])
        self.ops.append(['narrowExchange','treeModel','15.0'])
        self.ops.append(['wideExchange','treeModel','3.0'])
        self.ops.append(['wilsonBalding','treeModel','3.0'])
        self.ops.append(['scaleOperator','treeModel.rootHeight','0.75','5.0'])
        self.ops.append(['uniformOperator','treeModel.internalNodeHeights','30.0'])
        self.ops.append(['scaleOperator','luca_branch','0.2','1.0'])
        if demographic == "constant size":
            self.ops.append(['scaleOperator','constant.popSize','0.5','3.0'])
        elif demographic == "exponential growth":
            self.ops.append(['scaleOperator','exponential.popSize','0.5','3.0'])
            self.ops.append(['randomWalkOperator','exponential.growthRate','1.0','3'])                
        self.ops.append(['upDownOperator','clock.rate','treeModel.allInternalNodeHeights','0.75','5.0'])
        if datatype == "biallelicBinary" or datatype == "bb":
            self.ops.append(['scaleOperator','biallelicBinary.demethylation','0.25','0.25'])
            self.ops.append(['scaleOperator','biallelicBinary.homozygousMethylation','0.25','0.25'])
            self.ops.append(['scaleOperator','biallelicBinary.homozygousDemethylation','0.25','0.25'])
    ### PUBLIC INTERFACE #########        
    #---------------------------------------------------------------------------------
    def get_operators(self):
        ops = '<operators id="operators" optimizationSchedule="default">\n'
        for op in self.ops:
            if op[0] == "scaleOperator":
                ops += self._get_scaleOperator(op)
            elif op[0] == "upDownOperator":
                ops += self._get_upDownOperator(op)
            elif op[0] == "uniformOperator":
                ops += self._get_uniformOperator(op)
            elif op[0] == "wilsonBalding":
                ops += self._get_wilsonBalding(op)
            elif op[0] == "wideExchange":
                ops += self._get_wideExchange(op)
            elif op[0] == "narrowExchange":
                ops += self._get_narrowExchange(op)
            elif op[0] == "subtreeSlide":
                ops += self._get_subtreeSlide(op)
        ops += "</operators>\n"
        return ops
    #---------------------------------------------------------------------------------
    def _get_scaleOperator(self,op):
        idd,sf,we = op[1],op[2],op[3]        
        op = ""
        op += f'\t<scaleOperator scaleFactor="{sf}" weight="{we}">\n'
        op += f'\t\t<parameter idref="{idd}"/>\n'
        op += '\t</scaleOperator>\n'
        return op
        
    #---------------------------------------------------------------------------------
    def _get_upDownOperator(self,op):
        upid,downid,sf,we = op[1],op[2],op[3],op[4]
        op = ""
        op += f'\t<upDownOperator scaleFactor="{sf}" weight="{we}">\n'
        op += f'\t\t<up><parameter idref="{upid}"/></up>\n'
        op += f'\t\t<down><parameter idref="{downid}"/></down>\n'
        op += '\t</upDownOperator>\n'
        return op
    #---------------------------------------------------------------------------------
    def _get_uniformOperator(self,op):
        idd,we = op[1],op[2]        
        op = ""
        op += f'\t<uniformOperator weight="{we}">\n'
        op += f'\t\t<parameter idref="{idd}"/>\n'
        op += '\t</uniformOperator>\n'
        return op
    #---------------------------------------------------------------------------------
    def _get_wilsonBalding(self,op):
        idd,we = op[1],op[2]
        op = ""
        op += f'\t<wilsonBalding weight="{we}">\n'
        op += f'\t\t<treeModel idref="{idd}"/>\n'
        op += '\t</wilsonBalding>\n'
        return op
    #---------------------------------------------------------------------------------
    def _get_wideExchange(self,op):
        idd,we = op[1],op[2]
        op = ""
        op += f'\t<wideExchange weight="{we}">\n'
        op += f'\t\t<treeModel idref="{idd}"/>\n'
        op += '\t</wideExchange>\n'
        return op
    #---------------------------------------------------------------------------------
    def _get_narrowExchange(self,op):
        idd,we = op[1],op[2]
        op = ""
        op += f'\t<narrowExchange weight="{we}">\n'
        op += f'\t\t<treeModel idref="{idd}"/>\n'
        op += '\t</narrowExchange>\n'
        return op
    #---------------------------------------------------------------------------------
    def _get_subtreeSlide(self,op):         
        idd,size, gauss,we = op[1],op[2],op[3],op[4]
        op = ""
        op += f'\t<subtreeSlide  size="{size}" gaussian="{gauss}" weight="{we}">\n'
        op += f'\t\t<treeModel idref="{idd}"/>\n'
        op += '\t</subtreeSlide>\n'
        return op
    #---------------------------------------------------------------------------------
    #----------------------------------
    def get_operatorsx(self, demographic,datatype,clocks):
        if datatype == "bb":
            datatype = "biallelicBinary"
        op = ""
        op += '<operators id="operators" optimizationSchedule="default">\n'
        if datatype != "biallelicBinary":
            op += '\t<scaleOperator scaleFactor="0.25" weight="0.25">\n'
            op += f'\t\t<parameter idref="{datatype}.loss"/>\n'
            op += '\t</scaleOperator>\n'        
        op += '\t<scaleOperator scaleFactor="0.5" weight="10.0">\n'
        op += '\t\t<parameter idref="clock.rate"/>\n'
        op += '\t</scaleOperator>\n'                
        if clocks['type'] == "random local clock":
            op += '\t<scaleOperator scaleFactor="0.75" weight="15">\n'
            op += '\t\t<parameter idref="localClock.relativeRates"/>\n'
            op += '\t</scaleOperator>\n'        
            op += '\t<bitFlipOperator weight="15">\n'
            op += '\t\t<parameter idref="localClock.changes"/>\n'
            op += '\t</bitFlipOperator>\n'        
        op += '\t<subtreeSlide size="2.5" gaussian="true" weight="15.0"> <!-- 2.5 years. They will be automatically optimized by BEAST though -->\n'
        op += '\t\t<treeModel idref="treeModel"/>\n'
        op += '\t</subtreeSlide>\n'        
        op += '\t<narrowExchange weight="15.0">\n'
        op += '\t\t<treeModel idref="treeModel"/>\n'
        op += '\t</narrowExchange>\n'        
        op += '\t<wideExchange weight="3.0">\n'
        op += '\t\t<treeModel idref="treeModel"/>\n'
        op += '\t</wideExchange>\n'        
        op += '\t<wilsonBalding weight="3.0">\n'
        op += '\t\t<treeModel idref="treeModel"/>\n'
        op += '\t</wilsonBalding>\n'        
        op += '\t<scaleOperator scaleFactor="0.75" weight="5.0">\n'
        op += '\t\t<parameter idref="treeModel.rootHeight"/>\n'
        op += '\t</scaleOperator>\n'        
        op += '\t<uniformOperator weight="30.0">\n'
        op += '\t\t<parameter idref="treeModel.internalNodeHeights"/>\n'
        op += '\t</uniformOperator>\n'        
        op += '\t<scaleOperator scaleFactor="0.2" weight="1.0">\n'
        op += '\t\t<parameter idref="luca_branch"/>\n'
        op += '\t</scaleOperator>\n'        
        if demographic == "constant size":
            op += '\t<scaleOperator scaleFactor="0.5" weight="3.0">\n'
            op += '\t\t<parameter idref="constant.popSize"/>\n'
            op += '\t</scaleOperator>\n'
        elif demographic == "exponential growth":
            op += '\t<scaleOperator scaleFactor="0.5" weight="3.0">\n'
            op += '\t\t<parameter idref="exponential.popSize"/>\n'
            op += '\t</scaleOperator>\n'
            op += '\t<randomWalkOperator windowSize="1.0" weight="3">\n'
            op += '\t\t<parameter idref="exponential.growthRate"/>\n'
            op += '\t</randomWalkOperator>\n'                    
        op += '\t<upDownOperator scaleFactor="0.75" weight="5.0">\n'
        op += '\t\t<up>'
        op += '<parameter idref="clock.rate"/>'
        op += '</up>\n'
        op += '\t\t<down>'
        op += '<parameter idref="treeModel.allInternalNodeHeights"/>'
        op += '</down>\n'
        op += '\t</upDownOperator>\n'        
        if datatype == "biallelicBinary":
            op += '\t<scaleOperator scaleFactor="0.25" weight="0.25">\n'
            op += '\t\t<parameter idref="biallelicBinary.demethylation"/>\n'
            op += '\t</scaleOperator>\n'
            op += '\t<scaleOperator scaleFactor="0.25" weight="0.25">\n'
            op += '\t\t<parameter idref="biallelicBinary.homozygousMethylation"/>\n'
            op += '\t</scaleOperator>\n'
            op += '\t<scaleOperator scaleFactor="0.25" weight="0.25">\n'
            op += '\t\t<parameter idref="biallelicBinary.homozygousDemethylation"/>\n'
            op += '\t</scaleOperator>\n'
        op += '</operators>\n'                                
        return op