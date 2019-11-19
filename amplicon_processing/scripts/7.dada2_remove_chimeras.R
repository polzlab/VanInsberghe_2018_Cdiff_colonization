.libPaths(.libPaths()[2])
library(dada2)


seqtab <- readRDS(snakemake@input[["sequence_table_rds"]])
seqtab.nochim  <- removeBimeraDenovo(seqtab, method="consensus", multithread=TRUE, verbose=TRUE)
saveRDS(seqtab.nochim, snakemake@output[["sequence_table_rds"]])
write.csv(seqtab.nochim, snakemake@output[["sequence_table_csv"]])