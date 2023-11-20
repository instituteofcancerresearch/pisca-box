#!/opt/R/4.3.2/bin Rscript

#pdf("my_plot.pdf")
svg("my_plot2.svg")
plot(x = 1:10, y = 1:10)
abline(v = 0) 
text(x = 0, y = 1, labels = "Random text")
dev.off()
print("Succeeded")