import logging
from modules.loggingFunctions import initialize_logging
from modules.decorators import tojson, prefix, submit

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)

@tojson
@submit
@prefix
def query_db_status():
    '''
    Grabs all objectids having the relation.
    '''
    query = """
    SELECT DISTINCT ?spfyId ?Genome ?otype ?htype WHERE {{
        ?spfyId a :spfyId .
        ?spfyId (:hasPart|:isFoundIn) ?Genome .
        ?Genome a g:Genome.
        OPTIONAL {
            ?spfyId ge:0001076 ?otype .
            ?spfyId ge:0001077 ?htype .
        }
    }}
    """
    return query

if __name__ == "__main__":
    print query_everything()
