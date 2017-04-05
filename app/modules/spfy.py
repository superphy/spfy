#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import os

import redis
import config

from flask import current_app

# Redis Queue
from redis import Redis
from rq import Queue

# other libraries for rdflib
from rdflib import Graph



from modules.qc.qc import qc
from modules.blazeUploader.reserve_id import write_reserve_id
from modules.ectyper.call_ectyper import call_ectyper
from modules.amr.amr import amr
from modules.amr.amr_to_dict import amr_to_dict
from modules.beautify.beautify import beautify
from modules.turtleGrapher.datastruct_savvy import datastruct_savvy
from modules.turtleGrapher.turtle_grapher import turtle_grapher


# the only ONE time for global variables
# when naming queues, make sure you actually set a worker to listen to that queue
# we use the high priority queue for things that should be immediately
# returned to the user
redis_url = config.REDIS_URL
redis_conn = redis.from_url(redis_url)
singles_q = Queue('singles', connection=redis_conn)
multiples_q = Queue('multiples', connection=redis_conn, default_timeout=600)
blazegraph_q = Queue('blazegraph', connection=redis_conn)

def blob_savvy_enqueue(single_dict):
    '''
    Handles enqueueing of single file to multiple queues.
    :param f: a fasta file
    :param single_dict: single dictionary of arguments
    :return: dictionary with jobs ids and relevant headers
    '''
    jobs = {}
    query_file = single_dict['i']

    job_qc = multiples_q.enqueue(qc, query_file)
    job_id = blazegraph_q.enqueue(write_reserve_id, query_file, depends_on=job_qc)

    #### ECTYPER PIPELINE
    # the ectyper call is special in that it requires the entire arguments  to decide whether to carry the serotype option flag, virulance factors option flag, and percent identity field
    job_ectyper = singles_q.enqueue(call_ectyper, single_dict, depends_on=job_id)
    job_ectyper_beautify = multiples_q.enqueue(beautify, single_dict,query_file + '_ectyper.p', depends_on=job_ectyper, result_ttl=-1)
    job_ectyper_datastruct = multiples_q.enqueue(datastruct_savvy, query_file, query_file + '_id.txt', query_file + '_ectyper.p', depends_on=job_ectyper)
    #### END ECTYPER PIPELINE

    #### AMR PIPELINE
    job_amr = multiples_q.enqueue(amr, query_file, depends_on=job_id)
    job_amr_dict = multiples_q.enqueue(amr_to_dict, query_file + '_rgi.tsv', depends_on=job_amr)
    job_amr_beautify = multiples_q.enqueue(beautify, single_dict, query_file + '_rgi.tsv_rgi.p', depends_on=job_amr_dict, result_ttl=-1)
    job_amr_datastruct = multiples_q.enqueue(datastruct_savvy, query_file, query_file + '_id.txt', query_file + '_rgi.tsv_rgi.p', depends_on=job_amr)
    #### END AMR PIPELINE

    # the base file data for blazegraph
    job_turtle = multiples_q.enqueue(turtle_grapher, query_file, depends_on=job_qc)

    jobs[job_qc.get_id()] = {'file': single_dict['i'], 'analysis':'Quality Control'}
    jobs[job_id.get_id()] = {'file': single_dict['i'], 'analysis':'ID Reservation'}
    jobs[job_ectyper_beautify.get_id()] = {'file': single_dict['i'], 'analysis': 'Virulence Factors / Serotype'}
    jobs[job_amr_beautify.get_id()] = {'file': single_dict['i'], 'analysis': 'Antimicrobial Resistance'}

    return jobs

def blob_savvy(args_dict):
    '''
    Handles enqueuing of all files in a given directory or just a single file
    '''
    d = {}
    if os.path.isdir(args_dict['i']):
        for f in os.listdir(args_dict['i']):
            single_dict = dict(args_dict.items() + {'i': os.path.join(args_dict['i'], f)}.items())
            d.update(blob_savvy_enqueue(single_dict))
    else:
        d.update(blob_savvy_enqueue(args_dict))

    return d

def spfy(args_dict):
    '''
    '''
    # abs path resolution should be handled in spfy.py
    #args_dict['i'] = os.path.abspath(args_dict['i'])

    print 'Starting blob_savvy call'
    jobs_dict = blob_savvy(args_dict)

    return jobs_dict
