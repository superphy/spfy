#!/usr/bin/env python

"""Phylotyper module

Start phylotyper job

Example:
    :

        $ python phylotyper.py

"""

import os
import yaml
from datetime import datetime

__author__ = "Matthew Whiteside"
__copyright__ = "Copyright 2016, Public Health Agency of Canada"
__license__ = "APL"
__version__ = "2.0"
__maintainer__ = "Matthew Whiteside"
__email__ = "matthew.whiteside@phac-aspc.gc.ca"

import os
import pandas as pd
import cPickle as pickle

def pt_to_dict(pt_file):
    pt_results = pd.read_table(pt_file)
    pt_results = amr_results[['ORF_ID', 'START', 'STOP', 'ORIENTATION', 'CUT_OFF', 'Best_Hit_ARO']]

    pt_results.rename(
        columns={'ORF_ID': 'contig_id', 'Best_Hit_ARO': 'GENE_NAME'}, inplace=True)

    # sometimes there are spaces at the end of the contig id, also we remove
    # the additional occurance tag that RGI adds to contig ids
    amr_results['contig_id'] = amr_results['contig_id'].apply(
        lambda n: n.strip().rsplit('_', 1)[0])

    # note: you might be tempted to prefix a set_index('contig_id') but
    # remember, the same contig might have multiple genes
    amr_results = amr_results.to_dict(orient='index')

    # we have to manually check for contigs with multiple genes
    # TODO: write something less horrendously slow and memory consuming
    amr_dict = {}
    for i in amr_results.keys():
        contig_id = amr_results[i]['contig_id']
        if contig_id not in amr_dict.keys():
            amr_dict[contig_id] = []
        amr_dict[contig_id].append(dict((keys, amr_results[i][keys]) for keys in (
            'START', 'STOP', 'GENE_NAME', 'ORIENTATION', 'CUT_OFF', 'GENE_NAME')))

    amr_dict = {'Antimicrobial Resistance':amr_dict}

    p = os.path.join(amr_file + '_rgi.p')
    pickle.dump(amr_dict, open(p, 'wb'))

    return p

if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        help="Phylotyper .tsv results file",
        required=True
    )
    args = parser.parse_args()
    print pt_to_dict(args.i)