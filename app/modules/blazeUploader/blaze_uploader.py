import requests
import os
import rdflib
from app import config

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Literal
from app.modules.turtleGrapher.turtle_utils import generate_uri as gu

blazegraph_url = config.database['blazegraph_url']

def upload_graph(graph):
    """
    Uploads raw data onto Blazegraph. To ensure that Blazegraph interprets
    properly, it is necessary to specify the format in a Context-Header.

    Accepted formats are listed on this site:
    https://wiki.blazegraph.com/wiki/index.php/REST_API#MIME_Types

    Currently, the only data type needed is turtle, so this function is not
    usable for other formats.

    Args:
        data (turtle): a turtle data object

    Prints out the response object from Blazegraph
    """
    data = graph.serialize(format="turtle")

    headers = {'Content-Type': 'application/x-turtle'}
    request = requests.post(
        os.getenv(
            'SUPERPHY_RDF_URL',
            blazegraph_url
        ),
        data=data,
        headers=headers
    )
    return request.content

def check_duplicates(graph):
    '''
    
    :param graph: 
    :return: None if no duplicates found, otherwise return the duplicate's spfyID as a uriIsolate
    '''
    # retrieve the genome uri from the graph object; object=None to consider any object as valid
    uriGenome = next(graph.subjects(predicate=gu('so:0001462'), object=None))
    sparql = SPARQLWrapper(blazegraph_url)
    query = 'SELECT ?spfyid '
    query += 'WHERE { ?spfyid <' + gu('g:Genome') + '> ' + uriGenome + ' }'
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def check_largest_spfyid():
    sparql = SPARQLWrapper(blazegraph_url)
    query = 'SELECT ?spfyid'
    query += ' WHERE { ?spfyid <' + gu('g:Genome') + '> ?genomeid .'
    query += ' ?genomeid ' + gu('dc:date') + ' ?date }'
    query += ' ORDER BY DESC(?date) LIMIT 1'
    print 'query is :'
    print query
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def add_spfyid(graph, spfyid):
    uriIsolate = gu(':spfy' + str(spfyid))
    uriGenome = next(graph.subjects(predicate=gu('so:0001462'), object=None))
    # ex. :spfy234
    graph.add((uriIsolate, gu('rdf:type'), gu('ncbi:562')))
    graph.add((uriIsolate, gu('ge:0001567'), Literal("bacterium")))
    graph.add((uriIsolate, gu('dc:description'),
               Literal(uri_to_basename(uriIsolate))))

    # ex. :4eb02f5676bc808f86c0f014bbce15775adf06ba
    # associatting isolate URI with assembly URI
    graph.add((uriIsolate, gu('g:Genome'), uriGenome))
    return graph

def blaze_uploader(graph, spfyid = None):
    '''
    (1) Takes a rdflib.Graph object
    (2) Checks for duplicates in Blazegraph
        (2a.) If a duplicate is found, does a SPARQL Update with the new graph
        (2b.) Else: Queries Blazegraph for current largest spfyID
            (3) Appends the spfyID to the graph object
            (4) Uploads graph object to Blazegraph
    '''
    # setting the spfyID tells us to bypass all db checks and upload directly
    if not spfyid:
        duplicate = check_duplicates()
        if not duplicate:
            largest = check_largest_spfyid()
            graph = add_spfyid(largest,graph)
        else:
            raise Exception('Duplicate entry found in blazegraph: ' + duplicate)
    else:
        graph = add_spfyid(graph, spfyid)
    return upload_graph(graph)

if __name__=='__main__':
    print 'Testing...'
    print 'Largest Spfy ID:'
    print check_largest_spfyid()