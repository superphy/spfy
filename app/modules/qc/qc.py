import os
import tempfile
import subprocess
import argparse
import Bio.Blast.NCBIXML


def create_blast_db():
    '''
    Creates a reference database using https://raw.githubusercontent.com/superphy/version-1/master/Sequences/genome_content_panseq/putative_e_coli_specific.fasta
    The databse contains 10 ecoli-specific gene sequences
    '''
    ecoli_ref = 'putative_e_coli_specific.fasta'
    tempdir = tempfile.mkdtemp()
    blast_db_path = os.path.join(tempdir, 'ecoli_blastdb')

    completed_process = subprocess.call(["makeblastdb",
                                        "-in", ecoli_ref,
                                        "-dbtype", "nucl",
                                        "-title", "ecoli_blastdb",
                                        "-out", blast_db_path],
                                       check=True)
    if completed_process.returncode == 0:
        return blast_db_path
    else:
        raise


def run_blast(query_file, blast_db):
    blast_output_file = create_blast_db() + '.output'
    completed_process = subprocess.call(["blastn",
                                        "-query", query_file,
                                        "-db", blast_db,
                                        "-out", blast_output_file,
                                        "-outfmt", "5",
                                        "-word_size", "11"])
    if completed_process.returncode == 0:
        return blast_output_file
    else:
        raise


def qc(query_file):
    '''
    Compares the query_file against a reference db of ecoli-specific gene sequences.
    We consider a "pass" if the query_file has >=3 of the sequences.
    '''
    blast_db = create_blast_db()
    blast_output_file = run_blast(query_file, blast_db)

    print blast_output_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True)
    args = parser.parse_args()
    qc(args.i)
