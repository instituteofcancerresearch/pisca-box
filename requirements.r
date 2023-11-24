#!/opt/R/4.3.2/bin Rscript

print("=====================")
print("STARTING PACKAGE DOWNLOAD")
print("=====================")
list.of.packages <- c("jsonlite", "data.table","ggplot2","cowplot","HDInterval","HDInterval")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
print("=====================")
print(new.packages)
print("=====================")
if(length(new.packages)) install.packages(new.packages,dependencies=TRUE)#, repos='http://cran.rstudio.com/')

list.of.bio.packages <- c("treeio","ggtree")
new.bio.packages <- list.of.packages[!(list.of.bio.packages %in% installed.packages()[,"Package"])]
print("=====================")
print(new.bio.packages)
print("=====================")
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager",dependencies=TRUE)#, repos='http://cran.rstudio.com/')
if(length(new.bio.packages)) BiocManager::install(new.bio.packages)

#install.packages('ape',dependencies=TRUE, repos='http://cran.rstudio.com/')
#install.packages('jsonlite',dependencies=TRUE, repos='http://cran.rstudio.com/')
#install.packages('data.table',dependencies=TRUE, repos='http://cran.rstudio.com/')
#install.packages('ggplot2',dependencies=TRUE, repos='http://cran.rstudio.com/')
#install.packages('cowplot',dependencies=TRUE, repos='http://cran.rstudio.com/')
#install.packages('HDInterval',dependencies=TRUE, repos='http://cran.rstudio.com/')
#install.packages('lubridate',dependencies=TRUE, repos='http://cran.rstudio.com/')
# And from BIOCMANAGER
#install.packages('BiocManager',dependencies=TRUE, repos='http://cran.rstudio.com/')
#BiocManager::install('treeio')
#BiocManager::install('ggtree')