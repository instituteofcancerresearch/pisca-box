list.of.packages <- c("jsonlite", "data.table","ggplot2","cowplot","HDInterval","HDInterval", "randomForest", "KernSmooth", "Matrix", "cluster", "mgcv", "nlme")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
print(installed.packages())
if(length(new.packages)) install.packages(new.packages)


#list.of.packages <- c("treeio","ggtree")
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager",version="devel")



#BiocManager::install("tidytree", suppressUpdates=TRUE)
#install.packages("ape", dependencies = T)

#dependencies
BiocManager::install("ape", suppressUpdates=TRUE)

#BiocManager::install("treeio", suppressUpdates=TRUE)
#BiocManager::install("ggtree", suppressUpdates=TRUE)
