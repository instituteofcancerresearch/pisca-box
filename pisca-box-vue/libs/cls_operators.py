import pandas as pd
# ruff: noqa: E501
# ruff: noqa: F841
# ruff: noqa: F541

class Operators(object):
    def __init__(self,demographic,datatype,clocks):
        self.datatype = datatype
        self.datatype = demographic
        self.clocks = clocks
        self.ops = []
        
        # operator, paramater, weight, scaleFactor, size, gaussian
        
        self.ops.append(['scaleOperator','clock.rate','10.0','0.5','',''])
        self.ops.append(['subtreeSlide','treeModel','15.0','','2.5','true'])
        self.ops.append(['narrowExchange','treeModel','15.0','','',''])
        self.ops.append(['wideExchange','treeModel','3.0','','',''])
        self.ops.append(['wilsonBalding','treeModel','3.0','','',''])
        self.ops.append(['scaleOperator','treeModel.rootHeight','5.0','0.75','',''])
        self.ops.append(['uniformOperator','treeModel.internalNodeHeights','30.0','','',''])
        self.ops.append(['scaleOperator','luca_branch','1.0','0.2','',''])
        if demographic == "constant size":
            self.ops.append(['scaleOperator','constant.popSize','3.0','0.5','',''])
        elif demographic == "exponential growth":
            self.ops.append(['scaleOperator','exponential.popSize','3.0','0.5','',''])
            self.ops.append(['randomWalkOperator','exponential.growthRate', '3','1.0','',''])
        self.ops.append(['upDownOperator',  'clock.rate|treeModel.allInternalNodeHeights','5.0','0.75','',''])        
        if datatype == "biallelicBinary" or datatype == "bb":
            self.ops.append(['scaleOperator','biallelicBinary.demethylation','0.25','0.25','',''])
            self.ops.append(['scaleOperator','biallelicBinary.homozygousMethylation','0.25','0.25','',''])
            self.ops.append(['scaleOperator','biallelicBinary.homozygousDemethylation','0.25','0.25','',''])
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
        operator, paramater, weight, scaleFactor, size, gaussian = op[0],op[1],op[2],op[3],op[4],op[5]
        op = ""
        op += f'\t<scaleOperator scaleFactor="{scaleFactor}" weight="{weight}">\n'
        op += f'\t\t<parameter idref="{paramater}"/>\n'
        op += f'\t</scaleOperator>\n'
        return op
        
    #---------------------------------------------------------------------------------
    def _get_upDownOperator(self,op):
        operator, paramater, weight, scaleFactor, size, gaussian = op[0],op[1],op[2],op[3],op[4],op[5]
        up_p = paramater.split("|")[0]
        down_p = paramater.split("|")[1]
        op = ""
        op += f'\t<upDownOperator scaleFactor="{scaleFactor}" weight="{weight}">\n'
        op += f'\t\t<up><parameter idref="{up_p}"/></up>\n'
        op += f'\t\t<down><parameter idref="{down_p}"/></down>\n'
        op += f'\t</upDownOperator>'
        return op
    #---------------------------------------------------------------------------------
    def _get_uniformOperator(self,op):
        operator, paramater, weight, scaleFactor, size, gaussian = op[0],op[1],op[2],op[3],op[4],op[5]
        op = ""
        op += f'\t<uniformOperator weight="{weight}">\n'
        op += f'\t\t<parameter idref="{paramater}"/>\n'
        op += f'\t</uniformOperator>\n'
        return op
    #---------------------------------------------------------------------------------
    def _get_wilsonBalding(self,op):
        operator, paramater, weight, scaleFactor, size, gaussian = op[0],op[1],op[2],op[3],op[4],op[5]
        op = ""
        op += f'\t<wilsonBalding weight="{weight}">\n'
        op += f'\t\t<treeModel idref="{paramater}"/>\n'
        op += f'\t</wilsonBalding>\n'
        return op
    #---------------------------------------------------------------------------------
    def _get_wideExchange(self,op):
        operator, paramater, weight, scaleFactor, size, gaussian = op[0],op[1],op[2],op[3],op[4],op[5]
        op = ""
        op += f'\t<wideExchange weight="{weight}">\n'
        op += f'\t\t<treeModel idref="{paramater}"/>\n'
        op += f'\t</wideExchange>\n'
        return op
    #---------------------------------------------------------------------------------
    def _get_narrowExchange(self,op):
        operator, paramater, weight, scaleFactor, size, gaussian = op[0],op[1],op[2],op[3],op[4],op[5]
        op = ""
        op += f'\t<narrowExchange weight="{weight}">\n'
        op += f'\t\t<treeModel idref="{paramater}"/>\n'
        op += f'\t</narrowExchange>\n'
        return op
    #---------------------------------------------------------------------------------
    def _get_subtreeSlide(self,op):         
        operator, paramater, weight, scaleFactor, size, gaussian = op[0],op[1],op[2],op[3],op[4],op[5]
        op = ""
        op += f'\t<subtreeSlide  size="{size}" gaussian="{gaussian}" weight="{weight}">\n'
        op += f'\t\t<treeModel idref="{paramater}"/>\n'
        op += f'\t</subtreeSlide>\n'
        return op
    #---------------------------------------------------------------------------------
    def get_as_dataframe(self):                
        df = pd.DataFrame(self.ops,columns=['operator', 'parameter', 'weight', 'scaleFactor', 'size', 'gaussian'])
        return df
    #---------------------------------------------------------------------------------
    def update_from_dataframe(self,df):
        self.ops = []
        for row in df.itertuples():
            self.ops.append([row.operator,row.parameter,row.weight,row.scaleFactor,row.size,row.gaussian])                                
    #----------------------------------
    ############################################################################################################
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