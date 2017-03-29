import requests
import os
import rdflib

from app import config

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