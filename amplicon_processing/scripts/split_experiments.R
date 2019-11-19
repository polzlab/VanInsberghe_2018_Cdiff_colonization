library(tidyverse)
library(stringr)

write_split <- function(df, tax_filter_df, prefix) {
  filtered_df <- filter_seqtab(df, tax_filter_df)
  write_tables(filtered_df, prefix)
  write_taxonomy(filtered_df, prefix)
  write_asv_map(filtered_df, prefix)
  return(df)
}

filter_seqtab <- function(df, tax_filter_df) {
  df %>%
    inner_join(tax_filter_df, by=c("sequence"))
}

write_tables <- function(df, prefix){
  df %>%
    select(asv_id, count, sample) %>%
    spread(asv_id, count, fill=0) %>%
    write_csv(paste(paste0("output/to_share/", prefix), "count_table.csv", sep="_"))

  df %>%
    select(asv_id, count, sample) %>%
    group_by(sample) %>%
    mutate(rel = count/sum(count)) %>%
    select(-count) %>%
    ungroup() %>%
    spread(asv_id, rel, fill=0) %>%
    write_csv(paste(paste0("output/to_share/", prefix), "rel_table.csv", sep="_"))    
}

write_taxonomy <- function(df, prefix){
  df %>%
    select(asv_id,Kingdom,Phylum,Class,Order,Family,Genus,Species) %>%
    distinct %>%
    write_csv(paste(paste0("output/to_share/", prefix), "taxa.csv", sep="_"))
}


write_asv_map <- function(df, prefix){
  df %>% 
    select(asv_id, sequence) %>%
    distinct() %>%
    write_csv(paste(paste0("output/to_share/", prefix), "asv_map.csv", sep="_"))
}

df <- readRDS(snakemake@input[["sequence_table_rds"]]) %>% as.data.frame

asv_map <- read_csv(snakemake@input[["asv_map"]])

taxa_df <- readRDS(snakemake@input[["taxa_rds"]]) %>%
  as.data.frame %>%
  rownames_to_column("sequence") %>%
  as_tibble

joined_df <- df %>%
  as.data.frame %>%
  rownames_to_column("sample") %>%
  gather("sequence", "count", -sample) %>%
  left_join(asv_map, by="sequence")

tax_filter_df <- taxa_df %>%
  filter(!is.na(Kingdom))

joined_df %>%
  as_tibble %>%
  do(write_split(., tax_filter_df = tax_filter_df, prefix="Cdiff_PEG"))
