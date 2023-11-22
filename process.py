import gzip
import logging

# Constants
INPUT_FILE = 'data/input/Homo_sapiens.gene_info.gz'
OUTPUT_FILE = 'data/output/protein_coding_gene.csv'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
COLUMNS = ['GeneID', 'Symbol', 'chromosome', 'dbXrefs', 'type_of_gene']
DBXREF_KEYS = ['Ensembl', 'HGNC', 'MIM']

def extract_dbxref_values(dbxrefs, keys=DBXREF_KEYS):
    dbxref_dict = {key_val.split(':')[0]: ':'.join(key_val.split(':')[1:]) 
                   for key_val in dbxrefs.split('|') if ':' in key_val}
    return [dbxref_dict.get(key, '') for key in keys]

def parse_gene_info(input_file, output_file):
    try:
        with gzip.open(input_file, 'rt') as infile, open(output_file, 'w') as outfile:
            header = infile.readline().strip().split('\t')
            indices = {col: header.index(col) for col in COLUMNS}
            outfile.write('GeneID,Symbol,chromosome,Ensembl,HGNC,MIM\n')

            for line in infile:
                row = line.strip().split('\t')
                if row[indices['type_of_gene']] == 'protein-coding':
                    gene_info = [row[indices[col]] for col in ['GeneID', 'Symbol', 'chromosome']]
                    dbxrefs_values = extract_dbxref_values(row[indices['dbXrefs']])
                    outfile.write(','.join(gene_info + dbxrefs_values) + '\n')

        logging.info("File processing completed successfully.")
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        raise

def setup_logging():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def main():
    setup_logging()
    parse_gene_info(INPUT_FILE, OUTPUT_FILE)

if __name__ == '__main__':
    main()
