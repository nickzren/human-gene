# Human Gene

This repository processes NCBI gene information, extracting data for protein-coding genes, and saves it in a CSV file.

### Execution

```
conda env create -f environment.yml 

conda activate human-gene

bash download.sh

python process.py
```

### Input

- Homo_sapiens.gene_info.gz
  - The file from NCBI is a compressed archive containing detailed information on genes.

### Output

- protein_coding_gene.csv
  - The output file is a CSV containing extracted data on protein-coding genes from the NCBI dataset.