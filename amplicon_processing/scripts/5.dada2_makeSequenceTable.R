library(dada2)
denoised <- readRDS(snakemake@input[["f_denoised"]])

seqtab <- makeSequenceTable(f_denoised)

rownames(seqtab) <- paste(snakemake@wildcards[["plate"]],snakemake@wildcards[["sample"]],sep="_")

saveRDS(seqtab, snakemake@output[["sequence_table_rds"]])
