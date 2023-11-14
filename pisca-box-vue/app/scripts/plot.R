#!/usr/bin/env Rscript

#pdf("my_plot.pdf")
svg("my_plot.svg")
plot(x = 1:10, y = 1:10)
abline(v = 0) 
text(x = 0, y = 1, labels = "Random text")
dev.off()