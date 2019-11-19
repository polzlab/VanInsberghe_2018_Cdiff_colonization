library(dada2)

tables <- lapply(snakemake@input, readRDS)
tables <- tables[lapply(tables, length)>0]
combined <- do.call("mergeSequenceTables", tables)

print(combined)

saveRDS(combined, snakemake@output[["sequence_table_rds"]])
