import os
import logging
from datetime import datetime
from modules.turtleGrapher.turtle_utils import generate_hash, generate_uri as gu
from modules.blazeUploader.upload_graph import upload_graph
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Literal, Graph
import config
from modules.loggingFunctions import initialize_logging

log_file = initialize_logging()
log = logging.getLogger(__name__)

blazegraph_url = config.database['blazegraph_url']

def check_duplicates(uriGenome):
    '''
    Checks for duplicates in Blazegraph by computing genomeURI (the sha3(sorted content of file) from a graph object).
    :param graph:
    :return: None if no duplicates found, otherwise return the int of the duplicate's spfyID
    '''


    #SPARQL Query
    sparql = SPARQLWrapper(blazegraph_url)
    query = 'SELECT ?spfyid '
    query += 'WHERE { ?spfyid <' + gu(':hasPart') + '> <' + uriGenome + '> }'
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    log.debug(results)
    if not results['results']['bindings']:
        return None
    else:
        # ex. of result from Blazegraph:  {u'head': {u'vars': [u'spfyid']}, u'results': {u'bindings': [{u'spfyid': {u'type': u'uri', u'value': u'https://www.github.com/superphy#spfy2224'}}]}}
        # would return: 2224
        return int(results['results']['bindings'][0]['spfyid']['value'].split('spfy')[1])

def check_largest_spfyid():
    '''
    Checks the current largest spfyID is the database (via sort of insert timestamps).
    :return: (int)
    '''
    sparql = SPARQLWrapper(blazegraph_url)
    query = 'SELECT ?spfyid'
    query += ' WHERE { ?spfyid <' + gu(':hasPart') + '> ?genomeid .'
    query += ' ?genomeid <' + gu('dc:date') + '> ?date }'
    query += ' ORDER BY DESC(?date) LIMIT 1'
    log.debug(query)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    log.debug(results)
    # check that there was some result
    if results['results']['bindings']:
        # if there was a result, return the int of the spfyid
        return int(results['results']['bindings'][0]['spfyid']['value'].split('spfy')[1])
    else:
        # no result was found (fresh DB)
        return 0

def reservation_triple(uriGenome, spfyid):
    graph = Graph()

    uriIsolate = gu(':spfy' + str(spfyid))
    # se object type of spfyid
    graph.add((uriIsolate, gu('rdf:type'), gu(':spfyId')))

    # associatting isolate URI with assembly URI
    graph.add((uriIsolate, gu(':hasPart'), uriGenome))

    # timestamp
    now = datetime.now()
    now = now.strftime("%Y-%m-%d-%H-%M-%S-%f")
    graph.add((uriGenome, gu('dc:date'), Literal(now)))
    return graph

def reserve_id(query_file):
    '''
    given some fasta file:
    (1) Check for duplicates in blazegraph
    (2) If no duplicate is found, check for largest current spfyID
    (3) Create a triple (with associated timestamp) that links the fasta file hash to the spfyID
    (4) Upload that file to Blazegraph to reserve that spfyID
    (5) Return the spfyID to use in proceeding pipeline
    -> If a duplicate is found, just return that spfyID
    '''

    # uriGenome generation
    file_hash = generate_hash(query_file)
    uriGenome = gu(':' + file_hash)

    duplicate = check_duplicates(uriGenome)
    log.debug('check_duplicates() returned: ' + str(duplicate))
    if not duplicate:
        # no duplicates were found, check the current largest spfyID
        largest = check_largest_spfyid()
        # create a rdflib.graph object with the spfyID we want the new file to use
        graph = reservation_triple(uriGenome, largest+1)
        # uploading the reservation graph secures the file->spfyID link
        upload_graph(graph)
        # returns the (int) of the spfyID we want the new file to use
        return largest+1
    else:
        # a duplicate was found, return the (int) of it's spfyID
        return duplicate

def write_reserve_id(query_file):
    '''
    A write function for pipeline in spfy.py to write out file.
    :param query_file:
    :return:
    '''
    spfyid = reserve_id(query_file)
    log.info('SpfyID #:' + str(spfyid))
    id_file = os.path.abspath(query_file) + '_id.txt'
    with open(id_file, 'w+') as f:
        f.write(str(spfyid))
    return id_file
