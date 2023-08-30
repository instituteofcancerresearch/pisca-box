#Assuming an alignment has been made in Excel 

#e.g. Alignment_edited_by_eye.csv

alignment<-read.csv("IBD002/pisca-ibd002-21-deep/input/IBD002_21_deep_copynumbers_edit_by_eye.csv", header=F)

fasta<-alignment
dim(fasta)
rownames(fasta)<-fasta[,1]
fasta<-fasta[,-1]
str(fasta)
#fasta[36,]<-rep(2,2582)
#rownames(fasta)[21]<-"Diploid"

fasta[]<-lapply(fasta, function(x) gsub("10", "J", x))
fasta[]<-lapply(fasta, function(x) gsub("[0-9][0-9]", "J", x))
fasta[]<-lapply(fasta, function(x) gsub("0", "@", x))
fasta[]<-lapply(fasta, function(x) gsub("1", "A", x))
fasta[]<-lapply(fasta, function(x) gsub("2", "B", x))
fasta[]<-lapply(fasta, function(x) gsub("3", "C", x))
fasta[]<-lapply(fasta, function(x) gsub("4", "D", x))
fasta[]<-lapply(fasta, function(x) gsub("5", "E", x))
fasta[]<-lapply(fasta, function(x) gsub("6", "F", x))
fasta[]<-lapply(fasta, function(x) gsub("7", "G", x))
fasta[]<-lapply(fasta, function(x) gsub("8", "H", x))
fasta[]<-lapply(fasta, function(x) gsub("9", "I", x))

fasta[]<-lapply(fasta, function(x) gsub("X", "", x)) #remove X put in by me 
fasta_simple<-apply(fasta, 1, function(x) paste(x, collapse = ""))

#dat<-79.78
#can chage this with the actual dates later 
meta<-read.csv("IBD002/ibd002.csv") 
meta<-read.csv("../IBD003/ibd003.csv")
meta$decimaldate<-""
#loc<-meta[,c("Anatomical.location", "Tip_lab")]
#write.csv(rownames(fasta), "dates.csv")
dates<-read.csv("R_analysis/dates.csv")
#dat_loc<-merge(loc, dates, by='Tip_lab')
#write file out 
file<-"IBD002/pisca-ibd002-21-deep/stem.xml"
#cat("Hello",file=file,sep="\n")
#cat("World",file=file,append=TRUE)
cat("<beast>\n<taxa id=\"taxa\">\n", file=file, sep="\n")
#write the taxa block first 
for(i in 1:nrow(fasta)){
  cat(paste0("\t<taxon id=\"", rownames(fasta)[i] ,"\">"), file=file, sep="\n", append=T)
  #cat(paste0("\t\t<date value=\"", dat, "\" direction=\"forwards\" units=\"years\"/>	</taxon>"), file=file, sep="\n", append=T)
  cat(paste0("\t\t<date value=\"", dates$decimaldate[dates$Tip_lab_old==rownames(fasta)[i]], "\" direction=\"forwards\" units=\"years\"/>"), file=file, sep="\n", append=T)
  cat("\t\t<attr name=\"compartment\">", file=file, sep="\n", append=T)
  cat(paste0("\t\t\t", dates$compartment[dates$Tip_lab==rownames(fasta)[i]]),file=file, sep="\n", append=T)
  cat("\t\t</attr>", sep="\n", file=file, append=T)
  cat("\t\t</taxon>",sep="\n", file=file, append=T)
}
cat("</taxa>\n", file=file, append=T)

#alignment block 
#<alignment id="alignment">
#  <dataType idref="acna"/>
#  <sequence>
cat("<alignment id=\"alignment\">", file=file, sep='\n', append=T)  
cat("\t<dataType idref=\"acna\"/>", file=file, sep='\n', append=T)

for(i in 1:nrow(fasta)){
  cat("\t<sequence>", file=file, sep='\n', append=T)
  cat(paste0("<taxon idref=\"", rownames(fasta)[i], "\"/>") , file=file, sep="\n", append=T)
  cat(paste0("\t\t", fasta_simple[i]), file=file, sep="\n", append=T)
  cat("\t</sequence>", file=file, sep='\n', append=T)
}

cat("</alignment>", file=file, sep='\n', append = T)


## alternatively write a simple fasta file 

length(fasta_simple)
file<-"IBD002/pisca-ibd002-21-deep/simple.fasta"
fasta_simple<-as.data.frame(fasta_simple)
for(i in 1:nrow(fasta_simple)){
  cat(paste0(">", rownames(fasta_simple)[i]), file = file, sep='\n', append=T)
  cat(paste0(fasta_simple[i,1]), file=file, sep="\n", append=T)
}






