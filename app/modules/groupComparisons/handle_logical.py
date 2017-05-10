from modules.groupComparisons.logical_queries import resolve_spfyids, resolve_spfyids_negated

def handle_logical(group):
    '''
    Accepts a (list) group (of relations) as input and generates the results dictionary as required for fishers.
    '''
    # sanity check
    if type(group) not list:
        raise Exception("Invalid Argument. Requires a list of relation-attribute pairs for a group.")
    # create a blank universe which is our end result
    universe = set()
    for d, index in group:
        # create a temporary set before we merge with universe
        current_set = set()
        # d is of form: {"negated":false,"relation":"http://purl.obolibrary.org/obo/GENEPIO_0001076","attribute":"O136","logical":null}
        ### get the initial set
        if d['negated']:
            # get everything not d
            current_set = resolve_spfyids_negated(d['relation'], d['attribute'])
        else:
            # get spfyids in regular fashion
            current_set = resolve_spfyids(d['relation'], d['attribute'])
        print current_set

if __name__ == "__main__":
    d = {"negated":True,"relation":"http://purl.obolibrary.org/obo/GENEPIO_0001076","attribute":"O157"}
    handle_logical(d)
