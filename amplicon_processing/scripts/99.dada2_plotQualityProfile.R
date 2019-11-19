.libPaths(.libPaths()[2])
library(dada2)
library(ggplot2)

plot <- plotQualityProfile(snakemake@input[["fastq"]], n=5e4)
ggsave(filename=snakemake@output[["plot"]], plot=plot)