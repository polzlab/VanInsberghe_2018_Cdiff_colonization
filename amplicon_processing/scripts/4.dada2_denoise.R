library(dada2)

derep <- readRDS(snakemake@input[["derepped"]])
err_matrix <- readRDS(snakemake@input[["error_matrix"]])

denoised <- dada(derep, err=err_matrix, multithread=TRUE)

saveRDS(denoised, snakemake@output[["denoised"]])

seqtab <- makeSequenceTable(denoised)
rownames(seqtab) <- paste(snakemake@wildcards[["sample"]],snakemake@wildcards[["run_number"]],sep="_")
saveRDS(seqtab, snakemake@output[["sequence_table_rds"]])
