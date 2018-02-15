#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import os
import copy

import redis
import config

from flask import current_app

# Redis Queue
from redis import Redis
from rq import Queue

# other libraries for rdflib
from rdflib import Graph

from modules.qc.qc import qc
from middleware.blazegraph.reserve_id import write_reserve_id
from modules.ectyper.call_ectyper import call_ectyper_vf, call_ectyper_serotype
from modules.amr.amr import amr
from modules.amr.amr_to_dict import amr_to_dict
from middleware.display.beautify import beautify, model_to_json
from middleware.graphers.datastruct_savvy import datastruct_savvy
from middleware.graphers.turtle_grapher import turtle_grapher
from middleware.graphers.turtle_utils import actual_filename
from modules.phylotyper import phylotyper
from middleware.models import Pipeline

from modules.loggingFunctions import initialize_logging
import logging

# logging
initialize_logging()
logger = logging.getLogger(__name__)


# the only ONE time for global variables
# when naming queues, make sure you actually set a worker to listen to that queue
# we use the high priority queue for things that should be immediately
# returned to the user
redis_url = config.REDIS_URL
redis_conn = redis.from_url(redis_url)
singles_q = Queue('singles', connection=redis_conn)
multiples_q = Queue('multiples', connection=redis_conn,
                    default_timeout=config.DEFAULT_TIMEOUT)
blazegraph_q = Queue('blazegraph', connection=redis_conn)
if config.BACKLOG_ENABLED:
    # backlog queues
    backlog_singles_q = Queue('backlog_singles', connection=redis_conn)
    backlog_multiples_q = Queue(
        'backlog_multiples', connection=redis_conn, default_timeout=config.DEFAULT_TIMEOUT)

def _ectyper_pipeline_vf(singles, multiples, query_file, single_dict, pipeline=None):
    """
    Enqueue all the jobs required for VF.
    """
    # Dictionary of Job instances to return
    d = {}
    # Alias.
    job_id = pipeline.jobs['job_id']

    # Create a copy of the arguments dictionary and disable Serotype.
    # This copy is passed to the old ECTyper.
    single_dict_vf = copy.deepcopy(single_dict)
    single_dict_vf['options']['serotype'] = False
    # Enqueue the old ECTyper
    job_ectyper_vf = singles.enqueue(
        call_ectyper_vf,
        single_dict_vf,
        depends_on=job_id)
    d['job_ectyper_vf'] = job_ectyper_vf

    # If bulk uploading is set, we return the datastruct as the end task
    # to poll for job completion, therefore must set ttl of -1.
    if single_dict['options']['bulk']:
        ttl_value = -1
    else:
        ttl_value = config.DEFAULT_RESULT_TTL

    # datastruct_savvy() stores result to Blazegraph.
    job_ectyper_datastruct_vf = multiples.enqueue(
        datastruct_savvy,
        query_file,
        query_file + '_id.txt',
        query_file + '_ectyper_vf.p',
        depends_on=job_ectyper_vf,
        result_ttl=ttl_value)
    d['job_ectyper_datastruct_vf'] = job_ectyper_datastruct_vf

    if not single_dict['options']['bulk']:
        # Only bother parsing into json if user has requested either vf or
        # serotype, and we're not in bulk uploading.
        job_ectyper_beautify_vf = multiples.enqueue(
            beautify,
            query_file + '_ectyper.p',
            single_dict,
            depends_on=job_ectyper_vf,
            result_ttl=ttl_value
        )
        d['job_ectyper_beautify_vf'] = job_ectyper_beautify_vf

    return d

def _ectyper_pipeline_serotype(singles, multiples, query_file, single_dict, pipeline=None):
    """
    Enqueue all the jobs required for VF.
    """
    # Dictionary of Job instances to return
    d = {}
    # Alias.
    job_id = pipeline.jobs['job_id']

    # Create a copy of the arguments dictionary and disable Serotype.
    # This copy is passed to the old ECTyper.
    single_dict_vf = copy.deepcopy(single_dict)
    # Enqueue the new ECTyper
    job_ectyper_serotype = multiples.enqueue(
        call_ectyper_serotype,
        single_dict_vf,
        depends_on=job_id)
    d['job_ectyper_serotype'] = job_ectyper_serotype

    # If bulk uploading is set, we return the datastruct as the end task
    # to poll for job completion, therefore must set ttl of -1.
    if single_dict['options']['bulk']:
        ttl_value = -1
    else:
        ttl_value = config.DEFAULT_RESULT_TTL

    # datastruct_savvy() stores result to Blazegraph.
    job_ectyper_datastruct_serotype = multiples.enqueue(
        datastruct_savvy,
        query_file,
        query_file + '_id.txt',
        query_file + '_ectyper_serotype.p',
        depends_on=job_ectyper_serotype,
        result_ttl=ttl_value)
    d['job_ectyper_serotype'] = job_ectyper_datastruct_serotype

    if not single_dict['options']['bulk']:
        # Only bother parsing into json if user has requested either vf or
        # serotype, and we're not in bulk uploading.
        job_ectyper_beautify_serotype = multiples.enqueue(
            beautify,
            pickled_result = query_file + '_ectyper_serotype.p',
            depends_on=job_ectyper_serotype,
            result_ttl=ttl_value
        )
        d['job_ectyper_beautify_serotype'] = job_ectyper_beautify_serotype

    return d

def blob_savvy_enqueue(single_dict):
    '''
    Handles enqueueing of single file to multiple queues.
    :param f: a fasta file
    :param single_dict: single dictionary of arguments
        ex. {'i': '/datastore/2017-06-30-21-53-27-595283-GCA_000023365.1_ASM2336v1_genomic.fna', 'pi': 90, 'options': {'pi': 90, 'amr': False, 'serotype': True, 'vf': True}}}
        Where `options` is the user-selected choices for serotyping and
        the disable_* is used for running Ectyper; these are separate so we can
        always run ectyper in singles/backlog_singles while still returning to
        the user only what they selected.
    :return: dictionary with jobs ids and relevant headers
    '''
    jobs = {}
    query_file = single_dict['i']
    pipeline = Pipeline
    pipeline.single_dict = copy.deepcopy(single_dict)

    job_qc = multiples_q.enqueue(qc, query_file, result_ttl=-1)
    pipeline.jobs.update({'job_qc':job_qc})
    job_id = blazegraph_q.enqueue(
        write_reserve_id, query_file, depends_on=job_qc, result_ttl=-1)
    pipeline.jobs.update({'job_id':job_id})

    ## ECTyper (VF & Serotype)
    # VF
    if single_dict['options']['vf']:
        ectyper_vf_jobs = _ectyper_pipeline_vf(
            singles_q,
            multiples_q,
            query_file,
            single_dict,
            pipeline=pipeline
        )
        pipeline.jobs.update(ectyper_vf_jobs)
        if single_dict['options']['bulk']:
            ret_job_ectyper = ectyper_vf_jobs['job_ectyper_datastruct_vf']
            jobs[ret_job_ectyper.get_id()] = {
                'file': single_dict['i'],
                'analysis': 'Virulence Factors'}
        else:
            ret_job_ectyper = ectyper_vf_jobs['job_ectyper_beautify_vf']
            jobs[ret_job_ectyper.get_id()] = {
                'file': single_dict['i'],
                'analysis': 'Virulence Factors'}
    elif config.BACKLOG_ENABLED:
        # We need to create a dict with the options enabled.
        backlog_d = copy.deepcopy(single_dict)
        backlog_d['options']['vf'] = True
        # Explictedly set serotype to false in case of overlap.
        backlog_d['options']['serotype'] = False
        # Note: we use different queues.
        _ectyper_pipeline_vf(
            backlog_singles_q,
            backlog_multiples_q,
            query_file,
            backlog_d,
            pipeline=pipeline
        )

    # Serotype
    if single_dict['options']['serotype']:
        ectyper_serotype_jobs = _ectyper_pipeline_serotype(
            singles_q,
            multiples_q,
            query_file,
            single_dict,
            pipeline=pipeline
        )
        pipeline.jobs.update(ectyper_serotype_jobs)
        if single_dict['options']['bulk']:
            ret_job_ectyper = ectyper_serotype_jobs['job_ectyper_datastruct_serotype']
            jobs[ret_job_ectyper.get_id()] = {
                'file': single_dict['i'],
                'analysis': 'Serotype'}
        else:
            ret_job_ectyper = ectyper_serotype_jobs['job_ectyper_beautify_serotype']
            jobs[ret_job_ectyper.get_id()] = {
                'file': single_dict['i'],
                'analysis': 'Virulence Factors'}
    elif config.BACKLOG_ENABLED:
        # We need to create a dict with the options enabled.
        backlog_d = copy.deepcopy(single_dict)
        # Explictedly set vf to false in case of overlap.
        backlog_d['options']['vf'] = False
        backlog_d['options']['serotype'] = True
        _ectyper_pipeline_serotype(
           backlog_singles_q,
           backlog_multiples_q,
           query_file,
           backlog_d,
           pipeline=pipeline
        )
    # END ECTYPER PIPELINE

    # AMR PIPELINE
    def amr_pipeline(multiples):
        job_amr = multiples.enqueue(amr, query_file, depends_on=job_id)
        job_amr_dict = multiples.enqueue(
            amr_to_dict, query_file + '_rgi.tsv', depends_on=job_amr)
        # this uploads result to blazegraph
        if single_dict['options']['bulk']:
            job_amr_datastruct = multiples.enqueue(
                datastruct_savvy, query_file, query_file + '_id.txt', query_file + '_rgi.tsv_rgi.p', depends_on=job_amr_dict, result_ttl=-1)
        else:
            job_amr_datastruct = multiples.enqueue(
                datastruct_savvy, query_file, query_file + '_id.txt', query_file + '_rgi.tsv_rgi.p', depends_on=job_amr_dict)
        d = {'job_amr': job_amr, 'job_amr_dict': job_amr_dict,
             'job_amr_datastruct': job_amr_datastruct}
        # we still check for the user-selected amr option again because
        # if it was not selected but BACKLOG_ENABLED=True, we dont have to
        # enqueue it to backlog_multiples_q since beautify doesnt upload
        # blazegraph
        if single_dict['options']['amr'] and not single_dict['options']['bulk']:
            job_amr_beautify = multiples.enqueue(
                beautify,
                query_file + '_rgi.tsv_rgi.p',
                single_dict,
                depends_on=job_amr_dict,
                result_ttl=-1)
            d.update({'job_amr_beautify': job_amr_beautify})
        return d

    if single_dict['options']['amr']:
        amr_jobs = amr_pipeline(multiples_q)
        job_amr = amr_jobs['job_amr']
        job_amr_dict = amr_jobs['job_amr_dict']
        job_amr_datastruct = amr_jobs['job_amr_datastruct']
        if not single_dict['options']['bulk']:
            job_amr_beautify = amr_jobs['job_amr_beautify']
    elif config.BACKLOG_ENABLED:
        amr_pipeline(backlog_multiples_q)
    # END AMR PIPELINE

    # Phylotyper Pipeline
    def phylotyper_pipeline(multiples, subtype):

        jobname = '_pt' +subtype
        tsvfile = query_file + jobname + '.tsv'
        picklefile = query_file + jobname + '.p'

        job_pt = multiples.enqueue(
            phylotyper.phylotyper,
            None,
            subtype,
            tsvfile,
            id_file=query_file + '_id.txt',
            depends_on=pipeline.jobs['job_ectyper_datastruct_vf'])
        job_pt_dict = multiples.enqueue(
            phylotyper.to_dict, tsvfile, subtype, picklefile,
            depends_on=job_pt)
        job_pt_datastruct = multiples.enqueue(
            phylotyper.savvy, picklefile, subtype,
            depends_on=job_pt_dict)

        d = {'job'+jobname: job_pt, 'job'+jobname+'_dict': job_pt_dict,
             'job'+jobname+'_datastruct': job_pt_datastruct}
        # we still check for the user-selected amr option again because
        # if it was not selected but BACKLOG_ENABLED=True, we dont have to
        # enqueue it to backlog_multiples_q since beautify doesnt upload
        # blazegraph
        if single_dict['options'][subtype]:
            job_pt_beautify = multiples.enqueue(
                phylotyper.beautify, picklefile, actual_filename(query_file),
                depends_on=job_pt_dict, result_ttl=-1)
            d.update({'job'+jobname+'_beautify': job_pt_beautify})

        return d

    if single_dict['options']['stx1']:
        pt_jobs = phylotyper_pipeline(multiples_q, 'stx1')
        job_stx1_beautify = pt_jobs['job_ptstx1_beautify']
    elif config.BACKLOG_ENABLED:
        phylotyper_pipeline(backlog_multiples_q, 'stx1')

    if single_dict['options']['stx2']:
        pt_jobs = phylotyper_pipeline(multiples_q, 'stx2')
        job_stx2_beautify = pt_jobs['job_ptstx2_beautify']
    elif config.BACKLOG_ENABLED:
        phylotyper_pipeline(backlog_multiples_q, 'stx2')

    if single_dict['options']['eae']:
        pt_jobs = phylotyper_pipeline(multiples_q, 'eae')
        job_eae_beautify = pt_jobs['job_pteae_beautify']
    elif config.BACKLOG_ENABLED:
        phylotyper_pipeline(backlog_multiples_q, 'eae')
    # END Phylotyper pipeline

    # the base file data for blazegraph
    job_turtle = multiples_q.enqueue(
        turtle_grapher, query_file, depends_on=job_qc)

    jobs[job_qc.get_id()] = {'file': single_dict['i'],
                             'analysis': 'Quality Control'}
    jobs[job_id.get_id()] = {'file': single_dict['i'],
                             'analysis': 'ID Reservation'}

    # new to 4.3.3 if bulk ids used return the endpoint of datastruct generation
    # to poll for completion of all jobs
    # these two ifs handle the case where amr (or vf or serotype) might not
    # be selected but bulk is
    if single_dict['options']['amr']:
        ret_job_amr = job_amr_datastruct

    # Add the jobs to the return.
    # TODO: incorporate this into pipeline calls, as in the ECTYper pipeline.
    if single_dict['options']['amr']:
        jobs[ret_job_amr.get_id()] = {'file': single_dict[
            'i'], 'analysis': 'Antimicrobial Resistance'}
    if single_dict['options']['stx1']:
        jobs[job_stx1_beautify.get_id()] = {'file': single_dict[
            'i'], 'analysis': 'Phylotyper'}
    if single_dict['options']['stx2']:
        jobs[job_stx2_beautify.get_id()] = {'file': single_dict[
            'i'], 'analysis': 'Phylotyper'}
    if single_dict['options']['eae']:
        jobs[job_eae_beautify.get_id()] = {'file': single_dict[
            'i'], 'analysis': 'Phylotyper'}

    return jobs


def blob_savvy(args_dict):
    '''
    Handles enqueuing of all files in a given directory or just a single file
    '''
    d = {}
    if os.path.isdir(args_dict['i']):
        for f in os.listdir(args_dict['i']):
            single_dict = dict(args_dict.items() +
                               {'i': os.path.join(args_dict['i'], f)}.items())
            d.update(blob_savvy_enqueue(single_dict))
    else:
        d.update(blob_savvy_enqueue(args_dict))

    return d


def spfy(args_dict):
    '''
    '''
    # abs path resolution should be handled in spfy.py
    #args_dict['i'] = os.path.abspath(args_dict['i'])

    #print 'Starting blob_savvy call'
    #logger.info('args_dict: ' + str(args_dict))
    jobs_dict = blob_savvy(args_dict)

    return jobs_dict
