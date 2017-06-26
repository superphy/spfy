import logging
from modules.loggingFunctions import initialize_logging
from modules.decorators import toset, tolist, tostring, prefix, submit

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)

@submit
@prefix
def query_everything():
    '''
    Grabs all objectids having the relation.
    '''
    query = """
    SELECT DISTINCT ?spfyId ?Genome ?otype ?htype WHERE {{
        ?s a :spfyId .
        ?s (:hasPart|:isFoundIn) ?o .
        ?Genome a g:Genome.
        ?s ge:0001076 ?otype .
        ?s ge:0001077 ?htype .
    }}
    """
    return query

if __name__ == "__main__":
    print query_everything()
