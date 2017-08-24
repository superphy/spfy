"""Phylotyper module

Start phylotyper job. Uses default result directories

Example:
    :

        $ python example_google.py

"""

import subprocess
import os
import shutil
import logging
from tempfile import mkdtemp
import pandas as pd
import cPickle as pickle

import config
from modules.turtleGrapher import turtle_utils
from modules.phylotyper import ontology, exceptions
from modules.phylotyper.sequences import MarkerSequences

logger = logging.getLogger(__name__)



def phylotyper(query, subtype):
    '''
    Wrapper for Phylotyper

    Args:
        query (str): Genome URI
        subtype (str): Phylotyper recognized subtype (e.g. stx1)

    Returns:
        file to tab-delimited text results
    
    '''

    # Validate subtype ontology
    try:
        ontology.load(subtype)
    except exceptions.DatabaseError as err:
        logger.error('Please run VF detection before calling Phylotyper. Error message: {}'.format(err))
    except Exception as err:
        logger.error('Unexpected error from phylotyper ontology loading. Error message: {}'.format(err))
        raise err


    # Get loci to use in subtype prediction
    uri = 'subt:'+subtype
    loci_results = ontology.schema_query(uri)
    loci = [ turtle_utils.generate_uri(l['locus']) for l in sorted(loci_results, key=lambda k: k['i'])]

    # Get alleles for this genome
    markerseqs = MarkerSequences(loci)
    fasta = markerseqs.fasta(query)

    temp_dir = mkdtemp(prefix='pt', dir=config.DATASTORE)
    query_file = os.path.join(temp_dir, 'query.fasta')
    output_file = os.path.join(temp_dir, 'subtype_predictions.tsv')

    if fasta:
        # Run phylotyper
        with open(query_file, 'w') as fh:
            fh.write(fasta)

        subprocess.call(['phylotyper', 'genome', '--noplots',
                         subtype,
                         temp_dir,
                         query_file])

    else:
        # No loci
        # Report no loci status in output
        with open(output_file, 'w') as fh:
            fh.write("#Fake Header")
            fh.write("Required alleles not found")

    pt_file = query_file + '_pt.tsv'
    shutil.move(output_file, pt_file)
    shutil.rmtree(temp_dir)
          
    return pt_file


def phylotyper_to_dict(pt_file, subtype):
    """ Convert output into intermediate output

     dictionary indexed by 
    subtype predictions

    """
      
    pt_results = pd.read_table(pt_file)
    print(pt_results)

    pt_results = pt_results[['ORF_ID', 'START', 'STOP', 'ORIENTATION', 'CUT_OFF', 'Best_Hit_ARO']]


def phylotyper_savvy(pt_file, subtype):
    """ Load phylotyper results into DB

    """

    uri = 'subt:'+subtype


    # Get list of permissable subtype values
    subtypes_results = ontology.subtypeset_query(uri)
    subtypes = {}
    for r in subtypes_results:
        subtypes[ r['value'] ] = turtle_utils.generate_uri(r['part'])




if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-g",
        help="Genome URI",
        required=True
    )
    parser.add_argument(
        "-s",
        help="Phylotyper subtype scheme",
        required=True
    )
    args = parser.parse_args()
    phylotyper(args.g, args.s)