def handle_logical(group):
    '''
    Accepts a (list) group (of relations) as input and generates the results dictionary as required for fishers.
    '''
    # sanity check
    is type(group) not list and len(group) <= 1:
        raise Exception("Invalid Argument. Should run query directly.")
    # create a blank universe which is our end result
    universe = set()
    for d in group:
        # where d is of form: {"negated":false,"relation":"http://purl.obolibrary.org/obo/GENEPIO_0001076","attribute":"O136","logical":null}
        if d['negated']:
            # get everything not d
