import gzip
import logging
import csv
from collections import defaultdict

INPUT_FILE = 'data/input/Homo_sapiens.gene_info.gz'
PROTEIN_CODING_OUTPUT_FILE = 'data/output/protein_coding_gene.csv'
ALL_GENES_OUTPUT_FILE = 'data/output/all_gene.csv'
SUMMARY_OUTPUT_FILE = 'data/output/gene_type_summary.csv'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
COLUMNS = ['GeneID', 'Symbol', 'Synonyms', 'chromosome', 'dbXrefs', 'type_of_gene']
DBXREF_KEYS = ['Ensembl', 'HGNC', 'MIM']
EXCLUDE_TYPE = 'biological-region'

def extract_dbxref_values(dbxrefs, keys=DBXREF_KEYS):
    dbxref_dict = {key_val.split(':')[0]: ':'.join(key_val.split(':')[1:]) for key_val in dbxrefs.split('|') if ':' in key_val}
    return [dbxref_dict.get(key, '') for key in keys]

def parse_gene_info(input_file, protein_coding_output_file, all_genes_output_file, summary_output_file):
    gene_type_count = defaultdict(int)
    with gzip.open(input_file, 'rt') as infile, \
         open(protein_coding_output_file, 'w', newline='') as pc_outfile, \
         open(all_genes_output_file, 'w', newline='') as all_outfile:
        pc_writer = csv.writer(pc_outfile, quoting=csv.QUOTE_ALL)
        all_writer = csv.writer(all_outfile, quoting=csv.QUOTE_ALL)
        header = infile.readline().strip().split('\t')
        indices = {col: header.index(col) for col in COLUMNS}
        pc_writer.writerow(['GeneID', 'Symbol', 'Synonyms', 'chromosome', 'Ensembl', 'HGNC', 'MIM'])
        all_writer.writerow(['GeneID', 'Symbol', 'Synonyms', 'chromosome', 'Ensembl', 'HGNC', 'MIM', 'type_of_gene'])
        for line in infile:
            row = line.strip().split('\t')
            gene_info = [row[indices[col]] for col in ['GeneID', 'Symbol', 'Synonyms', 'chromosome']]
            dbxrefs_values = extract_dbxref_values(row[indices['dbXrefs']])
            type_of_gene = row[indices['type_of_gene']]
            gene_type_count[type_of_gene] += 1
            if type_of_gene != EXCLUDE_TYPE:
                all_writer.writerow(gene_info + dbxrefs_values + [type_of_gene])
            if type_of_gene == 'protein-coding':
                pc_writer.writerow(gene_info + dbxrefs_values)
    with open(summary_output_file, 'w', newline='') as summary_outfile:
        summary_writer = csv.writer(summary_outfile, quoting=csv.QUOTE_ALL)
        summary_writer.writerow(['type_of_gene', 'count'])
        for gene_type, count in gene_type_count.items():
            summary_writer.writerow([gene_type, count])
    logging.info("File processing completed successfully.")

def setup_logging():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def main():
    setup_logging()
    parse_gene_info(INPUT_FILE, PROTEIN_CODING_OUTPUT_FILE, ALL_GENES_OUTPUT_FILE, SUMMARY_OUTPUT_FILE)

if __name__ == '__main__':
    main()