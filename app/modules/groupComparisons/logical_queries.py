import config
import logging
import time
from modules.loggingFunctions import initialize_logging
from modules.turtleGrapher.turtle_utils import generate_uri as gu
from modules.groupComparisons.sparql_utils import generate_prefixes
from modules.groupComparisons.decorators import toset, tolist, prefix, submit

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)

@toset
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

def resolve_spfyids(relation, attribute):
    '''
    Args:
        relation: ex. "http://purl.obolibrary.org/obo/GENEPIO_0001076"
        attribute: ex. "O136"
    Ret:
    '''
    return query_single_objectid(relation, attribute)

if __name__ == "__main__":
    print resolve_spfyids(gu('ge:0001076'), 'O157')
