import requests
import os

import config

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
    blazegraph_url = config.database['blazegraph_url']
    
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


def upload_turtle(turtlefile):
    """
    Uploads raw data onto Blazegraph. To ensure that Blazegraph interprets
    properly, it is necessary to specify the format in a Context-Header.

    Accepted formats are listed on this site:
    https://wiki.blazegraph.com/wiki/index.php/REST_API#MIME_Types

    Currently, the only data type needed is turtle, so this function is not
    usable for other formats.

    Args:
        turtlefile(str): File path to turtle-format graph

    Returns response object from Blazegraph

    """
    blazegraph_url = config.database['blazegraph_url']

    response = None
    with open(turtlefile, 'r') as fh:
        data=fh.read()

        headers = {'Content-Type': 'application/x-turtle'}
        request = requests.post(
            blazegraph_url,
            data=data,
            headers=headers
        )
        response = request.content

    return response
