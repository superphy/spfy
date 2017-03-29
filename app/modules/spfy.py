#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import os

import redis
import app.config

from flask import current_app

# Redis Queue
from redis import Redis
from rq import Queue

# other libraries for rdflib
from rdflib import Graph



from app.modules.qc.qc import qc
from app.modules.blazeUploader.reserve_id import reserve_id
from app.modules.ectyper.call_ectyper import call_ectyper
from app.modules.amr.amr import amr
from app.modules.amr.amr_to_dict import amr_to_dict
from app.modules.beautify.beautify import beautify
from app.modules.turtleGrapher.datastruct_savvy import datastruct_savvy
from app.modules.blazeUploader.upload_graph import blaze_uploader
from app.modules.turtleGrapher.turtle_grapher import turtle_grapher


# the only ONE time for global variables
# when naming queues, make sure you actually set a worker to listen to that queue
# we use the high priority queue for things that should be immediately
# returned to the user
redis_url = app.config.REDIS_URL
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
    job_id = singles_q.enqueue(reserve_id, query_file, depends_on=job_qc)

    #### ECTYPER PIPELINE
    # the ectyper call is special in that it requires the entire arguments  to decide whether to carry the serotype option flag, virulance factors option flag, and percent identity field
    job_ectyper = singles_q.enqueue(call_ectyper, single_dict, depends_on=job_id)
    job_ectyper_beautify = multiples_q.enqueue(beautify, single_dict,query_file + '_ectyper.p', depends_on=job_ectyper, result_ttl=-1)
    job_ectyper_datastruct = multiples_q.enqueue(datastruct_savvy, single_dict, depends_on=job_ectyper)
    job_ectyper_blazegraph = blazegraph_q.enqueue(blaze_uploader, single_dict, depends_on=job_ectyper_datastruct)
    #### END ECTYPER PIPELINE

    #### AMR PIPELINE
    job_amr = multiples_q.enqueue(amr, query_file, depends_on=job_id)
    job_amr_dict = multiples_q.enqueue(amr_to_dict, query_file + '_rgi.tsv', depends_on=job_amr)
    job_amr_beautify = multiples_q.enqueue(beautify, query_file + '_rgi.tsv_rgi.p', depends_on=job_amr_dict, result_ttl=-1)
    job_amr_datastruct = multiples_q.enqueue(datastruct_savvy, single_dict, depends_on=job_amr)
    job_amr_blazegraph = blazegraph_q.enqueue(blaze_uploader, single_dict, depends_on=job_amr_datastruct)
    #### END AMR PIPELINE

    # the base file data for blazegraph
    job_turtle = multiples_q.enqueue(turtle_grapher, single_dict, depends_on=job_qc)
    job_turtle_blazegraph = blazegraph_q.enqueue(blaze_uploader, single_dict, depends_on=job_turtle)

    jobs[job_qc.get_id()] = {'file': single_dict['i'], 'analysis':'Quality Control'}
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
            single_dict = dict(args_dict.items() + {'i': os.path.abspath(f)}.items())
            d.update(blob_savvy_enqueue(single_dict))
    else:
        d.update(blob_savvy_enqueue(args_dict))

    return d

def spfy(args_dict):
    '''
    '''
    args_dict['i'] = os.path.abspath(args_dict['i'])

    print 'Starting blob_savvy call'
    jobs_dict = blob_savvy(args_dict)

    return jobs_dict

# ignore the super dangerous defining of a dictionary in arguments, this is only for testing
def spfy_test(args_dict={'i':'../tests/ecoli/GCA_001894495.1_ASM189449v1_genomic.fna', 's':1,'vf':1}):
    '''
    This is meant to mirror the pipeline, and for checking everything works together as expected w/o Redis Queue.
    '''

    args_dict['i'] = os.path.abspath(args_dict['i'])
    query_file = args_dict['i']

    print 'QC...'
    assert qc(query_file) == True
    print 'QC Done'

    print 'ECtyper...'
    #check that the results file will be where we expect
    assert call_ectyper(args_dict) == query_file +'_ectyper.p'
    print 'ECtyper done'

    print 'AMR...'
    assert amr(args_dict) == query_file + '.tsv'
    print 'AMR done'
    print 'AMR to Dict...'
    assert amr_to_dict(query_file + '.tsv') == query_file + '_amr.p'
    print 'AMR to Dict Done'

    print 'datastruct_savvy on ectyper...'


if __name__ == '__main__':
    '''
    You're not expected to call spfy.py directly!
    This is only meant for testing.
    '''
    spfy_test()