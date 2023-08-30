
#heather's version 
### script to make alignment files - alignment to read in microsoft excel 
files = Sys.glob("GAMBLE/analysis/*IBD002*single_pcf_segments.txt")

#IBD002 21 deep ones 
keep<-c(2,4,6,31,34,38,40,42,49, 50, 57, 58, 65, 66,68,69,70, 74, 76, 77, 81)

files<-files[keep]

# OKAY So 4398 is the number of bins. Got it. Good 
fileConn<-file("IBD002_21_deep_copynumbers.csv")
#writeLines(c("Hello","World"), fileConn)

for(x in 1:length(files)){
  
  sample_name<-files[x]
  sample_name<-gsub("GAMBLE/analysis/","",sample_name)
  sample_name<-gsub("_single_pcf_segments.txt","",sample_name)
  sample_name<- gsub("GC-MY-9485-", "",sample_name)
  sample_name<-gsub("GC-MY-9486-", "",sample_name)
  sample_name = gsub("-", "_", sample_name)
  string<-sample_name
  
  sample=as.data.frame(read.table(files[x], header=T))
  for(seg in 1:nrow(sample)){
    #chunk<-strrep(sample[seg,8], sample[seg,4], sep=',') #repeat the copy number by the bin number. 
    chunk<-paste(rep(sample[seg,8], sample[seg,4]), collapse=',')
    string<-paste(string, chunk, sep=',')
    #if(seg!= 1){
    #  if(sample[seg,1]!= sample[seg-1,1])
    #    string<-paste(string, "endofchromosome", sep=',')
    #}
  }
  #string<-paste(string, '\n', sep='') #add new line # Don't need this adding extra blanks 
  write(string, file='IBD002_21_deep_copynumbers.csv', append=TRUE)
}

close(fileConn)





