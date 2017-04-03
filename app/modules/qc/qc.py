import os
import tempfile
import subprocess
import argparse

import pandas as pd

# we want to use true division, not integer
#from __future__ import division

def create_blast_db():
    '''
    Creates a reference database using https://raw.githubusercontent.com/superphy/version-1/master/Sequences/genome_content_panseq/putative_e_coli_specific.fasta
    The databse contains 10 ecoli-specific gene sequences
    '''
    ecoli_ref = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/' + 'putative_e_coli_specific.fasta')
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
        raise Exception("Could not create blast db")


def run_blast(query_file, blast_db):
    '''
    Runs query against ref db of ecoli-spec sequences.
    Output format is set to '10'(csv)
    '''
    blast_output_file = create_blast_db() + '.output'
    ret_code = subprocess.call(["blastn",
                                        "-query", query_file,
                                        "-db", blast_db,
                                        "-out", blast_output_file,
                                        "-outfmt", '10 " qseqid qlen sseqid length pident sstart send sframe "',
                                        "-word_size", "11"])
    if ret_code == 0:
        return blast_output_file
    else:
        raise Exception("Could not run blast")

def parse_blast_records(blast_output_file):
    '''
    Recall, headers are: https://edwards.sdsu.edu/research/blast-output-8/
    For QC, we only consider perfect matches against our reference.

    returns a list of unique hits from the reference db
    '''
    blast_records = pd.read_csv(blast_output_file, header=None)
    blast_records.columns['qseqid','qlen','sseqid','length','pident','sstart','send','sframe']
    print blast_records
    # col 4 is percent identity, as set by our blast call above
    blast_records_pi_passed = blast_records[blast_records.iloc[:,4]>=90]

    # pl check: col
    blast_records_pi_pl_passed = blast_records_pi_passed[blast_records_pi_passed.iloc[:,3]/blast_records_pi_passed.iloc[:,1]>=90]

    # col 1 is the subject (where col 0 is the query)
    unique_hits = blast_records_pi_pl_passed.iloc[:,2].unique()

    return unique_hits

def qc(query_file):
    '''
    Compares the query_file against a reference db of ecoli-specific gene sequences.
    We consider a "pass" if the query_file has >=3 of the sequences.

    Returns True for pass, False for failed qc check (not ecoli.)
    '''
    blast_db = create_blast_db()
    blast_output_file = run_blast(query_file, blast_db)
    unique_hits = parse_blast_records(blast_output_file)

    if len(unique_hits) >= 3:
        return True
    else:
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True)
    args = parser.parse_args()
    print qc(args.i)
