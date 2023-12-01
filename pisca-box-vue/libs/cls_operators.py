import pandas as pd
# ruff: noqa: E501
# ruff: noqa: F841
# ruff: noqa: F541

class Operators(object):
    def __init__(self,demographic,luca_model,clocks,default_ops):                        
        self.ops = default_ops
        # operator, paramater, weight, scaleFactor, size, gaussian
        if demographic == "constant size":
            self.ops.append(['scaleOperator','constant.popSize','3.0','0.5','',''])
        elif demographic == "exponential growth":
            self.ops.append(['scaleOperator','exponential.popSize','3.0','0.5','',''])
            self.ops.append(['randomWalkOperator','exponential.growthRate', '3','1.0','',''])                
        if clocks["type"] == "random local clock":
            self.ops.append(['scaleOperator','localClock.relativeRates','15','0.75','',''])
            self.ops.append(['bitFlipOperator ','localClock.changes', '15','','',''])                
        if luca_model == "Neoplastic progression":
            self.ops.append(['scaleOperator','luca_branch','1.0','0.2','',''])
            self.ops.append(['upDownOperator',  'clock.rate|treeModel.allInternalNodeHeights,luca_branch','5.0','0.75','',''])
        else:
            self.ops.append(['upDownOperator',  'clock.rate|treeModel.allInternalNodeHeights','5.0','0.75','',''])
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
            elif op[0] == "bitFlipOperator ":
                ops += self._get_bitFlip(op)
        ops += "</operators>\n"
        return ops
    #---------------------------------------------------------------------------------
    def getOpsList(self):
        #create list from priors and operators
        ops = []
        for op in self.ops:
            if op[1] not in ops:
                ops.append(op[1])
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
        up_ps = paramater.split("|")[0].split(",")
        down_ps = paramater.split("|")[1].split(",")
        op = ""
        op += f'\t<upDownOperator scaleFactor="{scaleFactor}" weight="{weight}">\n'
        
        op += f'\t\t<up>\n'
        for up_p in up_ps:        
            op += f'\t\t\t<parameter idref="{up_p}"/>\n'
        op += f'\t\t</up>\n'
        
        op += f'\t\t<down>\n'
        for down_p in down_ps:        
            op += f'\t\t\t<parameter idref="{down_p}"/>\n'
        op += f'\t\t</down>\n'
        
        op += f'\t</upDownOperator>\n'
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
    def _get_bitFlip(self,op):
        operator, paramater, weight, scaleFactor, size, gaussian = op[0],op[1],op[2],op[3],op[4],op[5]
        op = ""
        op += f'\t<bitFlipOperator  weight="{weight}">\n'
        op += f'\t\t<parameter idref="{paramater}"/>\n'
        op += f'\t</bitFlipOperator>\n'
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
    
    