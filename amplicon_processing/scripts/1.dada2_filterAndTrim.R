# sample-wise filtering using dada2.

library(dada2)

filterAndTrim(
    fwd=snakemake@input[["forward"]], filt=snakemake@output[["forward"]],
    rev =snakemake@input[["reverse"]], filt.rev =snakemake@output[["reverse"]],
    maxN=snakemake@params[["maxN"]], maxEE=snakemake@params[["maxEE"]], truncQ=snakemake@params[["truncQ"]],
    truncLen=c(snakemake@params[["truncLen_forward"]], snakemake@params[["truncLen_reverse"]]),
    compress=TRUE, verbose=TRUE
)

if (!file.exists(snakemake@output[["forward"]])){{
    file.create(snakemake@output[["forward"]])
}}

if (!file.exists(snakemake@output[["reverse"]])){{
    file.create(snakemake@output[["reverse"]])
}}