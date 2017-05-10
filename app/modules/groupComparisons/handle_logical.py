import logging
from modules.loggingFunctions import initialize_logging
from modules.groupComparisons.logical_queries import resolve_spfyids, resolve_spfyids_negated

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)

def handle_logical(group):
    '''
    Accepts a (list) group (of relations) as input and generates the results dictionary as required for fishers.
    '''
    # sanity check
    if type(group) is not list:
        raise Exception("Invalid Argument. Requires a list of relation-attribute pairs for a group.")
    # create a blank universe which is our end result
    universe = set()
    for index, d in enumerate(group):
        # create a temporary set before we merge with universe
        current_set = set()
        # d is of form: {"negated":false,"relation":"http://purl.obolibrary.org/obo/GENEPIO_0001076","attribute":"O136","logical":null}
        ### get the initial set
        if d['negated']:
            # get everything not d
            log.info('Handling negation for pair: ' + d['relation'] + d['attribute'])
            current_set = resolve_spfyids_negated(d['relation'], d['attribute'])
        else:
            # get spfyids in regular fashion
            current_set = resolve_spfyids(d['relation'], d['attribute'])

if __name__ == "__main__":
    d = [{"negated":True,"relation":"http://purl.obolibrary.org/obo/GENEPIO_0001076","attribute":"O157"}]
    handle_logical(d)
