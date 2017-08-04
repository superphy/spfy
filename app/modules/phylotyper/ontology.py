"""Check and Setup Phylotyper Ontology and Subtyping Schemes


Example:
    $ python ontolog.py -s stx1

"""

import logging
import os

from modules.turtleGrapher.turtle_utils import generate_uri as gu
from modules.decorators import submit, prefix
from modules.blazeUploader import upload_turtle, upload_graph

log = logging.getLogger(__name__)
typing_ontology_version = '<https://www.github.com/superphy/typing/1.0.0>'
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

@submit
def version_query(version):
    """
    Queries for a given typing ontology version

    returns:
        dictionary

    """
    query = '''
        SELECT ?version
        WHERE {
            ?version rdf:type owl:Ontology .
            ?version owl:versionIRI {version}
        }
        '''.format(version=version)

    return query


@submit
@prefix
def subtype_query(subtype):
    """
    Queries for a phylotyper subtype definition

    returns:
        dictionary

    """
    query = '''
        SELECT ?subtype
        WHERE {
            ?subtype rdf:type subt:Phylotyper .
            VALUES ?subtype { subt:{subtype} }
        }
        '''.format(subtype)

    return query


def match_version(version):
    """
    Returns true if ontology with given version is already in database

    Args:
        version(str): ontology version string e.g. <https://www.github.com/superphy/typing/1.0.0>

    """
   
    result = version_query(version)

    if 'version' in result['results']['bindings']:
        return True
    else:
        return False


def match_subtype(subtype_uri):
    """
    Returns true if subtype URI is already in database

    Args:
        subtype(str): subtype URI (adds typing ontology prefix for you)

    """
   
    result = subtype_query(subtype_uri)

    if 'subtype' in result['results']['bindings']:
        return True
    else:
        return False


def stx1_graph():
    """
    Returns graph object that defines stx1 phylotyper subtype schema

    """

    pass


def stx2_graph():
    """
    Returns graph object that defines stx2 phylotyper subtype schema

    """

    pass


def eae_graph():
    """
    Returns graph object that defines eae phylotyper subtype schema

    """

    pass


def load(subtype):
    """
    Loads typing ontology and schema for a given phylotyper subtype

    Args:
        subtype(str): A subtype name that matches one of the defined subtype initialization methods in this module

    Returns:
        None

    """

    func_name = subtype+'_graph'

    if not func_name in globals():
        raise ValueError("Undefined subtype: {}".format(subtype))
    graph_func = globals()[func_name]
   
    ontology_turtle_file = os.path.join(__location__, 'superphy_subtyping.ttl')
    
    if not match_version(typing_ontology_version):
        log.info('Uploading subtyping ontolog version: {}'.format(typing_ontology_version))
        response = upload_turtle(ontology_turtle_file)
        log.info('Upload returned response: {}'.format(response))

    if not match_subtype(subtype):
        log.info('Uploading subtype definition: {}'.format(subtype))
        graph = graph_func()
        response = upload_graph(graph)
        log.info('Upload returned response: {}'.format(response))

    # Database ready to recieve phylotyper data for this subtype



if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        help="Phylotyper subtype scheme",
        required=True
    )
    args = parser.parse_args()

    load(args.s)

    