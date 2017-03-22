#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import logging
import os

import redis
import config

from flask import current_app

# Redis Queue
from redis import Redis
from rq import Queue

# other libraries for rdflib
from rdflib import Graph

# our own slightly more general stuff
from modules.turtleGrapher.turtle_utils import generate_uri as gu, generate_hash

# for various features we add
from savvy import savvy  # serotype/amr/vf



from config import database
from multiprocessing import Pool, cpu_count


# the only ONE time for global variables
# when naming queues, make sure you actually set a worker to listen to that queue
# we use the high priority queue for things that should be immediately
# returned to the user
redis_url = config.REDIS_URL
redis_conn = redis.from_url(redis_url)
high = Queue('high', connection=redis_conn)
low = Queue('low', connection=redis_conn, default_timeout=600)


def blob_savvy(args_dict):
    '''
    Handles savvy.py's pipeline.
    '''
    d = {}
    if os.path.isdir(args_dict['i']):
        for f in os.listdir(args_dict['i']):
            single_dict = dict(args_dict.items() + {'uriIsolate': args_dict['uris'][f][
                               'uriIsolate'], 'uriGenome': args_dict['uris'][f]['uriGenome'], 'i': args_dict['i'] + f, 'uris': None}.items())
            job_high= high.enqueue(savvy, dict(single_dict.items() +
                                     {'disable_amr': True}.items()),result_ttl=-1)
            job_low = low.enqueue(savvy, dict(single_dict.items() +
                                    {'disable_vf': True, 'disable_serotype': True}.items()),result_ttl=-1)
            d[job_high.get_id()] = {'file':f, 'analysis':'Virulence Factors / Serotype'}
            d[job_low.get_id()] = {'file':f, 'analysis': 'Antimicrobial Resistance'}
    else:
        # run the much faster vf and serotyping separately of amr
        job_high = high.enqueue(savvy, dict(args_dict.items() +
                                 {'disable_amr': True}.items()),result_ttl=-1)
        job_low = low.enqueue(savvy, dict(args_dict.items() +
                                {'disable_vf': True, 'disable_serotype': True}.items()),result_ttl=-1)
        d[job_high.get_id()] = {'file':args_dict['i'], 'analysis':'Virulence Factors and Serotype'}
        d[job_low.get_id()] = {'file':args_dict['i'], 'analysis': 'Antimicrobial Resistance'}

    return d

def spfyids_single(args_dict):

    # this is temporary, TODO: include a spqarql query to the db
    uriIsolate = gu(':spfy' + str(database['count']))

    uriGenome = gu(':' + generate_hash(args_dict['i']))

    args_dict['uriIsolate'] = uriIsolate
    args_dict['uriGenome'] = uriGenome

    return args_dict


def hash_me(file_dict):
    uris = {}
    uris[file_dict['basename']] = {}
    uris[file_dict['basename']]['uriIsolate'] = gu(
        ':spfy' + str(file_dict['count']))
    uris[file_dict['basename']]['uriGenome'] = gu(
        ':' + generate_hash(file_dict['withpath']))
    return uris


def spfyids_directory(args_dict):
    '''
    TODO: make the database count actually work
    This is meant to preallocate spfyIDs
    -note may have problems with files that fail (gaps in id range)
    TODO: fix that^
    TODO: make this whole thing less messy
    '''


    print 'Precomputing hashes for all files in directory, may take awhile...'

    files = os.listdir(args_dict['i'])
    count = database['count']

    # inital mapping of a files to a number(spfyID)
    files_list = []
    for f in files:
        file_dict = {}
        file_dict['basename'] = f
        file_dict['withpath'] = args_dict['i'] + f
        file_dict['count'] = count
        files_list.append(file_dict)
        count += 1
    # TODO: write-out count

    # hasing and make uris
    p = Pool(cpu_count())
    # this will return a list of dicts
    uris = p.map(hash_me, files_list)

    # convert the list of dicts into a nested dict structure {filename:
    # {'uriIsolate' , 'uriGenome'}}
    # ducttape soln
    uris_dict = {}
    for uri_dict in uris:
        uris_dict[uri_dict.keys()[0]] = uri_dict.values()[0]

    args_dict['uris'] = uris_dict

    return args_dict


def spfy(args_dict):
    '''
    '''
    # check if a directory was passed or a just a single file
    # updates args_dict with appropriate rdflib.URIRef's
    if os.path.isdir(args_dict['i']):
        if args_dict['i'][-1] is not '/':
            args_dict['i'] = args_dict['i'] + '/'
        args_dict = spfyids_directory(args_dict)
    else:
        args_dict = spfyids_single(args_dict)

    print 'Starting blob_savvy call'
    logging.info('Starting blob_savvy call...')
    jobs_dict = blob_savvy(args_dict)
    logging.info('blob_savvy enqueues finished')

    return jobs_dict

if __name__ == "__main__":
    import argparse

    # parsing cli-input
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        help="FASTA file or directory",
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

    args = parser.parse_args()
    # we make a dictionary from the cli-inputs and add are uris to it
    # mainly used for when a func needs a lot of the args
    args_dict = vars(args)

    # starting logging
    # TODO: move this to global and see it if breaks
    logging.basicConfig(
        filename='outputs/spfy' + __name__ + '.log',
        level=logging.INFO
    )

    spfy(args_dict)

    print('ALL COMPLETE')
    logging.info('ALL COMPLETE')
