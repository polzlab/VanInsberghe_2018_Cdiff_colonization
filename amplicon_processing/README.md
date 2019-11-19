## Installation of dependencies

### Install miniconda3 on your system if needed

```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh
```

type `which conda` to make sure it's in your `PATH`. If not, try running `conda init` and restarting your terminal.

### Create a conda environment
```
conda create --name dada2pipeline -c conda-forge -c R -c bioconda r-base=3.4 r-tidyverse snakemake;
conda activate dada2pipeline;
```

### Install dada2 version 1.6 in R

```
# activate conda environment
conda activate dada2pipeline;
# launch R (should be version 3.4.3)
R
# Install dada2 (hit no when bioconductor asks to update packages)
source("https://bioconductor.org/biocLite.R")
BiocInstaller::biocLite(c("dada2"))
# Check dada2 version
library(dada2)
sessionInfo()
# under other attached packages, should see [1] dada2_1.6.0 
```

## Running the pipeline

In order to run the dada2 pipeline on a single machine, activate the conda environment and run snakemake with the `dada2_pseudopool.snake` file:

```
conda activate dada2pipeline;
snakemake -s dada2_pseudopool.snake
```

To run this pipeline on an HPC cluster, please see the snakemake documentation at [https://snakemake.readthedocs.io/en/stable/executing/cluster-cloud.html#cluster-execution](https://snakemake.readthedocs.io/en/stable/executing/cluster-cloud.html#cluster-execution). Feel free to open an issue on this repository with any questions.


