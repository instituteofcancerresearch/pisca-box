#!/usr/bin/env Rscript

library(data.table)
library(ggplot2)
library(cowplot)
library(treeio)
library(ggtree)
library(HDInterval)
library(lubridate)

#Configuration 
burnin=0.1
ppThreshold=0.8


#args=commandArgs(trailingOnly = T)
args=c(paste0(folder, "input/rlc-exp.mcc"),
        paste0(folder, "input/ibd-rlc-exp.log"),
        paste0(folder, "Test.plot.pdf"),
       "Title of plot",
       "68"
       )

#TODO I need to get the tree and the logs merged, not only from one replicate
##TODO Check the args
mccTreeFile=args[1]
logDataFile=args[2]
outputfile=args[3]
title=args[4]
age=as.numeric(args[5])

#Parsing cenancestor information from the log file
logData=fread(logDataFile)
#lucaBranch=mean(logData[,luca_branch][floor(nrow(logData)*burnin):nrow(logData)])
lucaBranch=age
lucaHeight=mean(logData[,luca_height][floor(nrow(logData)*burnin):nrow(logData)])
hpdLucaHeight=hdi(logData[,luca_height][floor(nrow(logData)*burnin):nrow(logData)],credMass = 0.95)
lucaRate=mean(logData[,cenancestorRate][floor(nrow(logData)*burnin):nrow(logData)])

rm(logData)

##Parsing the tree
mccTree=read.beast(mccTreeFile)
mccTreeDataFrame=fortify(mccTree)

##Tree-dependent time calculation
yearsToAdd=age-max(mccTreeDataFrame[,"x"])

#Adding luca with proper time
root=which(mccTreeDataFrame$parent==mccTreeDataFrame$node)
luca=nrow(mccTreeDataFrame)+1
mccTreeDataFrame[luca,]=mccTreeDataFrame[root,]
mccTreeDataFrame[root,]=mccTreeDataFrame[luca,]
mccTreeDataFrame[root,"parent"]=luca
mccTreeDataFrame[root,"branch.length"]=yearsToAdd
mccTreeDataFrame[luca,"x"]=max(mccTreeDataFrame[,"x"])-age
mccTreeDataFrame[luca,"node"]=luca

#Modifying times from time from the present to time from birth
mccTreeDataFrame$x=mccTreeDataFrame$x+yearsToAdd
mccTreeDataFrame$branch=mccTreeDataFrame$branch+yearsToAdd
mostRecentYearsOfAge=max(mccTreeDataFrame$x)
mccTreeDataFrame$height_0.95_HPD=lapply(mccTreeDataFrame$height_0.95_HPD,function(x){return(c(mostRecentYearsOfAge-x[2],mostRecentYearsOfAge-x[1]))})
mccTreeDataFrame$height_0.95_HPD[luca]=list(as.numeric(c(mostRecentYearsOfAge-hpdLucaHeight[2],mostRecentYearsOfAge-hpdLucaHeight[1])))

#Adding PP info
mccTreeDataFrame$posteriorAsterisk=as.character(ifelse(mccTreeDataFrame$posterior>=ppThreshold,"*",""))

#Removing PP data for LUCA
mccTreeDataFrame[luca,"posteriorAsterisk"]=NA
mccTreeDataFrame[luca,"posterior"]=NA

#Removing PP data for MRCA
mccTreeDataFrame[root,"posteriorAsterisk"]=NA
mccTreeDataFrame[root,"posterior"]=NA

#add CEnRate 
mccTreeDataFrame[luca,"rate"]=lucaRate

#Plotting
#########

#Adjusting x limits to make sure tip names are shown completely
minX=min(mccTreeDataFrame[,"x"])
maxX=max(mccTreeDataFrame[,"x"])
extraX=0.2*(maxX-minX)
padMinX=2

minXError=min(as.vector(sapply(mccTreeDataFrame$height_0.95_HPD,function(x){return(c(x[1],x[2]))},simplify = TRUE)),na.rm = T)

#Getting y information
mccTreePlot=ggplot(mccTreeDataFrame,aes(x=x,y=y))+geom_tree(size=1.5)+
  theme_tree2(legend.position=c(0.1,0.7))+
  geom_nodelab(aes(label=round(posterior,2)),hjust=-.1,vjust=1.8,color="black") + ##PP values
  geom_range("height_0.95_HPD", color='black', size=5, alpha=.3) + #HPD height
  geom_tiplab(align = FALSE,color="black",size=5,hjust=-0.2) +
  labs(title=title) + 
  theme(plot.title= element_text(size = rel(2.5),hjust = 0.5),axis.text.x=element_text(size=rel(1.5)),axis.title.x=element_text(size=rel(1.5))) +
  scale_x_continuous(name="Patient age (years)",limits=c(min(minX,minXError)-padMinX,maxX+extraX))
mccTreePlot

mccTreeDataFrame$rate<-as.numeric(mccTreeDataFrame$rate)

tryrates=TRUE ## try to get the colour branches 
if(tryrates){
mccTreePlot=ggplot(mccTreeDataFrame,aes(x=x,y=y))+ geom_tree(size=1.5, aes(color=rate))  +
  scale_color_continuous(low="darkgreen", high="red") +
  theme_tree2(legend.position=c(0.1,0.7))+
  geom_nodelab(aes(label=round(posterior,2)),hjust=-.1,vjust=1.8,color="black") + ##PP values
  geom_range("height_0.95_HPD", color='black', size=5, alpha=.3) + #HPD height
  geom_tiplab(align = FALSE,color="black",size=5,hjust=-0.2) +
  labs(title=title) + 
  theme(plot.title= element_text(size = rel(2.5),hjust = 0.5),axis.text.x=element_text(size=rel(1.5)),axis.title.x=element_text(size=rel(1.5))) +
  scale_x_continuous(name="Patient age (years)",limits=c(min(minX,minXError)-padMinX,maxX+extraX))
}


save_plot(plot = mccTreePlot,filename = outputfile,base_height = 5,base_aspect_ratio = 1.6)

