.libPaths(.libPaths()[2])
library(dada2)
library(tidyverse)

derep <- readRDS(snakemake@input[["derepped"]])
err_matrix <- readRDS(snakemake@input[["error_matrix"]])
old_seqtab <- readRDS(snakemake@input[["sequence_table_rds"]])

priors <- old_seqtab %>%
  as.data.frame %>%
  rownames_to_column("sample") %>%
  gather("sequence", "count", -sample) %>%
  group_by(sequence) %>%
  filter(count > 0) %>%
  filter(n() > 1) %>%
  select(sequence) %>% distinct %>%
  pull(sequence)
  

denoised <- dada(derep, err=err_matrix, priors=priors, multithread=TRUE)

saveRDS(denoised, snakemake@output[["denoised"]])