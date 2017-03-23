#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

# use: python savvy.py -i samples/ANLJ01.1.fsa_nt

# S:erotype
# A:ntimicrobial Resistance
# V:irulence Factors
# -vy

import logging

from app.modules.turtleGrapher.turtle_utils import generate_uri as gu
from app.modules.turtleGrapher.turtle_grapher import generate_graph, generate_hash, generate_turtle_skeleton

from app.modules.blazeUploader.blaze_uploader import upload_graph
from app.modules.beautify.beautify import json_return

from app.modules.ectyper.call_ectyper import call_ectyper

# for pairwise comparison of rows in panadas

def savvy(args_dict):
    '''
    Args:
        args_dict(dict): i prefer working with args in a dictionary, rather than a namespace is all

    Returns:
        (rdflib.Graph): a graph object with the VF/AMR/Serotype added to it via ECTyper/RGI
    '''
    from os import remove  # for batch cleanup
    # starting #logging
    '''
    logging.basicConfig(
        filename='outputs/' + __name__ +
        args_dict['i'].split('/')[-1] + '.log',
        level=logging.INFO
    )
    '''

    print("Importing FASTA from: " + args_dict['i'])
    #logging.info('importing from' + args_dict['i'])

    #saving copy of filename, this is req due to hack used to handle ectyper
    args_dict['filename'] = args_dict['i']

    # setting up graph
    graph = generate_graph()

    ectyper_result={}

    #logging.info('generating barebones ttl from file')
    graph = generate_turtle_skeleton(
        graph, args_dict['i'], args_dict['uriIsolate'], args_dict['uriGenome'])
    #logging.info('barebones ttl generated')

    if not (args_dict['disable_serotype'] and args_dict['disable_vf'] and args_dict['disable_amr']):
        #logging.info('calling ectyper')
        ectyper_result = call_ectyper(graph, args_dict)
        graph = ectyper_result['graph']
        #logging.info('ectyper call completed')

    # individual fasta logs are wiped on completion (or you'd have several
    # thousand of these)
    #remove('outputs/' + __name__ + args_dict['i'].split('/')[-1] + '.log')
    print upload_graph(graph)

    if not (args_dict['disable_serotype'] and args_dict['disable_vf'] and args_dict['disable_amr']):
        return json_return(args_dict, ectyper_result['ectyper_dict'])

if __name__ == "__main__":
    import argparse
    import os  # for batch cleanup

    from ConfigParser import SafeConfigParser

    # parsing cli-input
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        help="FASTA file",
        required=True
    )
    parser.add_argument(
        "--disable-serotype",
        help="Disables use of the Serotyper. Serotyper is triggered by default.",
        action="store_true"
    )
    parser.add_argument(
        "--disable-vf",
        help="Disables use of ECTyper to get associated Virulence Factors. VFs are computed by default.",
        action="store_true"
    )
    parser.add_argument(
        "--disable-amr",
        help="Disables use of RGI to get Antimicrobial Resistance Factors.  AMR genes are computed by default.",
        action="store_true"
    )
    # note: by in large, we expect uri to be given as just the unique string
    # value  (be it the hash or the integer) without any prefixes, the actual
    # rdflib.URIRef object will be generated in this script
    # this is mainly for batch computation
    parser.add_argument(
        "--uriGenome",
        help="Allows the specification of the Genome URI separately. Expect just the hash (not an actual uri).",
    )
    # This is both for batch computation and for future extensions where there
    # are multiple sequencings per isolate (Campy)
    parser.add_argument(
        "--uriIsolate",
        help="Allows the specification of the Isolate URI separately. Expect just the integer (not the full :spfyID)",
        type=int
    )
    args = parser.parse_args()
    # we make a dictionary from the cli-inputs and add are uris to it
    # mainly used for when a func needs a lot of the args
    args_dict = vars(args)

    # starting#logging
    '''
    logging.basicConfig(
        filename='outputs/' + __name__ +
        args_dict['i'].split('/')[-1] + '.log',
        level=logging.INFO
    )
    '''

    # check if a genome uri isn't set yet
    if args_dict['uriIsolate'] is None:
        # this is temporary, TODO: include a spqarql query to the db
        uriIsolate = gu(':spfy' + str(hash(args_dict['i'].split('/')[-1])))
    else:
        uriIsolate = gu(':spfy' + args_dict['uriIsolate'])

    # if the fasta_file hash was not precomputed (batch scripts should
    # precompute it), we compute that now
    if args_dict['uriGenome'] is None:
        uriGenome = gu(':' + generate_hash(args_dict['i']))
    else:
        uriGenome = gu(':' + args_dict['uriGenome'])

    args_dict['uriIsolate'] = uriIsolate
    args_dict['uriGenome'] = uriGenome

    print savvy(args_dict)
