library(tidyverse)
library(stringr)

df <- readRDS(snakemake@input[["sequence_table_rds"]])

df %>% as.data.frame %>%
  rownames_to_column("sample") %>% 
  gather("sequence","count", -sample) %>%
  select(sequence) %>% distinct %>%
  bind_cols(asv_id = group_indices(., sequence)) %>%
  select(asv_id, sequence) %>%
  arrange(asv_id) %>%
  mutate(asv_id=paste0("ASV",str_pad(asv_id, 5, pad = "0"))) %>%
  write_csv(snakemake@output[["asv_map"]])