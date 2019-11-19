.libPaths(.libPaths()[2])
library(tidyverse)
library(dada2)

prepooled_df <- read_csv(snakemake@input[["sequence_table_csv"]])

prior_seqs <- prepooled_df %>%
    separate(col=X1, into=c("plate", "sample"), sep="_", convert=TRUE) %>% 
    mutate(sample=if_else(sample=="NTC", paste(plate, sample,sep="_"), sample)) %>%
    gather("sequence", "count", -sample) %>%

derep <- readRDS(snakemake@input[["derepped"]])
err_matrix <- readRDS(snakemake@input[["error_matrix"]])

denoised <- dada(derep, err=err_matrix, multithread=TRUE)

saveRDS(denoised, snakemake@output[["denoised"]])