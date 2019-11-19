.libPaths(.libPaths()[2])
library(dada2)
#print(snakemake@input)


tables <- lapply(snakemake@input, readRDS)
#tables <- tables[lapply(tables, length)>0]
combined <- do.call("mergeSequenceTables", tables)

saveRDS(combined, snakemake@output[["sequence_table_rds"]])
#write.csv(combined, snakemake@output[["sequence_table_csv"]])
#uniquesToFasta(combined, snakemake@output[["uniques_fasta"]])