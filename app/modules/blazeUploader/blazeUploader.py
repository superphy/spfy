import requests
import os
import config

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph

def upload_graph(graph, url='http://localhost:8080/bigdata/sparql'):
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
            url
        ),
        data=data,
        headers=headers
    )
    return request.content

def blazeUploader(graph, blazegraph_url, spfyid = None):
    '''
    (1) Takes a rdflib.Graph object
    (2) Checks for duplicates in Blazegraph
    (3) Queries Blazegraph for current largest spfyID
    (4) Appends the spfyID to the graph object
    (5) Uploads graph object to Blazegraph
    '''

    # (5)
    upload_graph(graph, blazegraph_url)
