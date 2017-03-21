import os
import tempfile
import subprocess
import argparse
import Bio.Blast.NCBIXML

import pandas as pd

def create_blast_db():
    '''
    Creates a reference database using https://raw.githubusercontent.com/superphy/version-1/master/Sequences/genome_content_panseq/putative_e_coli_specific.fasta
    The databse contains 10 ecoli-specific gene sequences
    '''
    ecoli_ref = 'putative_e_coli_specific.fasta'
    tempdir = tempfile.mkdtemp()
    blast_db_path = os.path.join(tempdir, 'ecoli_blastdb')

    ret_code = subprocess.call(["makeblastdb",
                                        "-in", ecoli_ref,
                                        "-dbtype", "nucl",
                                        "-title", "ecoli_blastdb",
                                        "-out", blast_db_path])
    if ret_code == 0:
        return blast_db_path
    else:
        raise


def run_blast(query_file, blast_db):
    blast_output_file = create_blast_db() + '.output'
    ret_code = subprocess.call(["blastn",
                                        "-query", query_file,
                                        "-db", blast_db,
                                        "-out", blast_output_file,
                                        "-outfmt", "10",
                                        "-word_size", "11"])
    if ret_code == 0:
        return blast_output_file
    else:
        raise

def parse_blast_records(blast_output_file):
    blast_records = pd.read_csv(blast_output_file)
    print blast_records
    print blast_records.iloc[:,2]


def qc(query_file):
    '''
    Compares the query_file against a reference db of ecoli-specific gene sequences.
    We consider a "pass" if the query_file has >=3 of the sequences.
    '''
    blast_db = create_blast_db()
    blast_output_file = run_blast(query_file, blast_db)
    print blast_output_file
    parse_blast_records(blast_output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True)
    args = parser.parse_args()
    qc(args.i)
