library(dada2)

err_matrix <- learnErrors(snakemake@input, nbases=snakemake@config[["nbases"]], multithread=snakemake@threads)
saveRDS(err_matrix, snakemake@output[["error_matrix"]])
