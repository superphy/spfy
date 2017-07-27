"""Phylotyper module

Start phylotyper job. Start phylotyper job. Uses default result directories

Example:
    :

        $ python example_google.py

"""

import subprocess
import os
import shutil

from backports import tempfile

def phylotyper(query_file, subtype):
    '''
    Wrapper for Phylotyper

    Args:
        query_file (str): Input file
        subtype (str): Phylotyper recognized subtype (e.g. stx1)

    Returns:
        file to tab-delimited text results
    
    '''

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
    args = parser.parse_args()
    print amr(args.i)