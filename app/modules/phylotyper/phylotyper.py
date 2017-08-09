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

from backports import tempfile

import ontology
import exceptions

logger = logging.getLogger(__name__)

def phylotyper(query, subtype):
    '''
    Wrapper for Phylotyper

    Args:
        query (str): Spfy ID
        subtype (str): Phylotyper recognized subtype (e.g. stx1)

    Returns:
        file to tab-delimited text results
    
    '''

    # Validate subtype ontology
    try:
        ontology.load(subtype)
    except exceptions.DatabaseException as err:
        logger.error('Please run VF detection before calling Phylotyper. Error message: {}'.format(err))
    except Exception as err:
        logger.error('Unexpected error from phylotyper ontology loading. Error message: {}'.format(err))
        raise err


    output_dir = os.path.dirname(query_file)

    with tempfile.TemporaryDirectory(dir=output_dir) as temp_dir:

        subprocess.call(['phylotyper', 'genome', '--noplots',
                         subtype,
                         temp_dir,
                         query_file])


    # rename and move the tsv to the original directory, if applicable
    pt_file = os.path.join(outputdir)
    shutil.move(outputname+'.txt', amr_file)

    return amr_file

if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        help="FASTA file",
        required=True
    )
    parser.add_argument(
        "-s",
        help="Phylotyper subtype scheme",
        required=True
    )
    args = parser.parse_args()
    print amr(args.i)