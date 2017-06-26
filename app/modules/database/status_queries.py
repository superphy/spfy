import logging
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
    SELECT DISTINCT ?s ?o WHERE {{
        ?s (:hasPart|:isFoundIn) ?o .
    }}
    """
    return query

if __name__ == "__main__":
    print query_everything()
