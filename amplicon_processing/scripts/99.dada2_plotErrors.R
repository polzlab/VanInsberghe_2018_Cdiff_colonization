.libPaths(.libPaths()[2])
library(dada2)
library(ggplot2)

err <- readRDS(snakemake@input[["error_matrix"]])

p <- plotErrors(err, nominalQ=TRUE)

ggsave(filename=snakemake@output[["plot"]], plot=p)
