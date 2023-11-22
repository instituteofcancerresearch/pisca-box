#!/opt/R/4.3.2/bin Rscript


# Call this as follows:
# Rscript pisca-plot.R consensus.tree my_pisca.log my_plot.pdf 'MY TITLE' 68

suppressWarnings({

library(data.table)
library(ggplot2)
library(cowplot)
library(treeio)
library(ggtree)
library(HDInterval)
library(lubridate)
library(svglite)

#Configuration
burnin=0.1
ppThreshold=0.8

folder = getwd()

args=commandArgs(trailingOnly = T)
#args=c(paste0(folder, "/input/rlc-exp.mcc"),
#        paste0(folder, "/input/ibd-rlc-exp.log"),
#        paste0(folder, "Test.plot.pdf"),
#        "Title of plot",
#        "68"
#        )

#TODO I need to get the tree and the logs merged, not only from one replicate
##TODO Check the args
#print(args)
mccTreeFile=args[1]
age=as.numeric(args[2])
lucaHeight = as.numeric(args[3])
hpdLucaHeight_l = as.numeric(args[4])
hpdLucaHeight_u = as.numeric(args[5])
lucaRate = as.numeric(args[6])
useRate = args[7]
outputfile=args[8]
title=args[9]
#logDataFile=args[10]

print(paste("mccfile",mccTreeFile))
print(paste("age",age))
print(paste("lucaHeight",lucaHeight))
print(paste("hpdLucaHeight_l",hpdLucaHeight_l))
print(paste("hpdLucaHeight_u",hpdLucaHeight_u))
print(paste("lucaRate",lucaRate))
print(paste("useRate",useRate))
print(paste("outputfile",outputfile))
print(paste("title",title))
#print(paste("logfile",logDataFile))
hpdLucaHeight <- c(hpdLucaHeight_l,hpdLucaHeight_u)
print(paste("Luca hdi=",hpdLucaHeight))


#Parsing cenancestor information from the log file
#logData=fread(logDataFile)
#lucaBranch=mean(logData[,luca_branch][floor(nrow(logData)*burnin):nrow(logData)])
lucaBranch=age

#lucaheight = 0
#hpdLucaHeight = 0
#lucaRate = 0

#lucaHeight=mean(logData[,luca_height][floor(nrow(logData)*burnin):nrow(logData)])
#hpdLucaHeight=hdi(logData[,luca_height][floor(nrow(logData)*burnin):nrow(logData)],credMass = 0.95)



tryrates=FALSE ## try to get the colour branches 
if (useRate == "Y"){
  tryrates=TRUE
  print("cenancestor exists")
}

#rm(logData)

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


if(tryrates){
  #add CEnRate   
  mccTreeDataFrame[luca,"rate"]=lucaRate
  mccTreePlot=ggplot(mccTreeDataFrame,aes(x=x,y=y))+ geom_tree(size=1.5, aes(color=rate))  +
    scale_color_continuous(low="blue", high="red") +
    theme_tree2(legend.position=c(0.1,0.7))+
    geom_nodelab(aes(label=round(posterior,2)),hjust=-.1,vjust=1.8,color="black") + ##PP values
    geom_range("height_0.95_HPD", color='black', size=5, alpha=.3) + #HPD height
    geom_tiplab(align = FALSE,color="black",size=5,hjust=-0.2) +
    labs(title=title) + 
    theme(plot.title= element_text(size = rel(2.5),hjust = 0.5),axis.text.x=element_text(size=rel(1.5)),axis.title.x=element_text(size=rel(1.5))) +
    scale_x_continuous(name="Patient age (years)",limits=c(min(minX,minXError)-padMinX,maxX+extraX))
}


print("saving plot")
save_plot(plot = mccTreePlot,filename = outputfile,base_height = 5,base_aspect_ratio = 1.6)

})