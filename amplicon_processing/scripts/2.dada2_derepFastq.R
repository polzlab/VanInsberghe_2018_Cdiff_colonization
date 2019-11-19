library(dada2)

derep <- derepFastq(snakemake@input[["filtered"]])
saveRDS(derep, snakemake@output[["derepped"]])