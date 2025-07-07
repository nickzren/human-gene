# Human Gene

This repository processes NCBI gene information, extracting data for protein-coding genes, and saves it in a CSV file.

### Execution

```
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run the pipeline
bash download.sh
uv run python process.py
```

### Input

- Homo_sapiens.gene_info.gz
  - The file from NCBI is a compressed archive containing detailed information on genes.

### Output

- protein_coding_gene.csv
  - The output file is a CSV containing extracted data on protein-coding genes from the NCBI dataset.