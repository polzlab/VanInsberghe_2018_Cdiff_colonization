.libPaths(.libPaths()[2])
library(dada2)
f_denoised <- readRDS(snakemake@input[["f_denoised"]])
f_derepped <- readRDS(snakemake@input[["f_derepped"]])
r_denoised <- readRDS(snakemake@input[["r_denoised"]])
r_derepped <- readRDS(snakemake@input[["r_derepped"]])

#merged <- mergePairs(f_denoised, f_derepped, r_denoised, r_derepped, returnRejects=TRUE)
concat <- mergePairs(f_denoised, f_derepped, r_denoised, r_derepped, minOverlap=8)
#merged[!merged$accept,] <- concat[!merged$accept,]

seqtab <- makeSequenceTable(concat)

# set the sample name to the rownames for merging the tables from multiple samples later
rownames(seqtab) <- snakemake@wildcards[["sample_and_run_number"]]

saveRDS(seqtab, snakemake@output[["sample_sequence_table"]])
