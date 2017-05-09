import config
import logging
import time
from modules.loggingFunctions import initialize_logging
from modules.turtleGrapher.turtle_utils import generate_uri as gu
from modules.groupComparisons.sparql_utils import generate_prefixes
from modules.groupComparisons.decorators import toset, tolist, tostring, prefix, submit

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)

@tostring
@submit
@prefix
def query_single_objectid(relation, attribute):
    '''
    Grabs a single object id having the relation.
    '''
    query = """
    SELECT ?s WHERE {{
        ?s <{relation}> '{attribute}' .
    }}
    LIMIT 1
    """.format(relation=relation,attribute=attribute)
    return query

@tolist
@submit
@prefix
def query_objecttypes(uri):
    '''
    Grabs the types of a given uri.
    '''
    query = """
    SELECT ?s WHERE {{
        <{uri}> a ?s .
    }}
    """.format(relation=relation,attribute=attribute)
    return query

def resolve_spfyids(relation, attribute):
    '''
    Args:
        relation: ex. "http://purl.obolibrary.org/obo/GENEPIO_0001076"
        attribute: ex. "O136"
    Ret:
    '''
    objectid = query_single_objectid(relation, attribute)
    print objectid
    objectype = query_objecttypes(objectid)
    print objectype

if __name__ == "__main__":
    resolve_spfyids(gu('ge:0001076'), 'O157')
