from modules.groupComparisons.handle_logical import handle_logical
from modules.groupComparisons.logical_queries import query_targets
from modules.groupComparisons.fishers import fishers

def collapse(dict_targets):
    '''
    Collapses all targets into a dictionary mapping each target to a set of the spfyIds its found in.
    Arg:
        dict_targets: (dict) of structure {spfyid: set(targets)}
    '''
    # define the base dictionary
    d = {}
    for spfyid, set_targets in dict_targets.iteritems():
        for target in set_targets:
            if target not in d.keys():
                # then that gene has not spfyId assoc. with it yet
                d[target] = set(spfyid)
            else:
                d[target].add(spfyid)
    return d

def groupcomparisons(groups, target):
    # define a list of sets to hold all spfyids per group
    sets_spfyids = []
    # define a list of nested dictionaries mapping spfyid to all of its targets
    # this ends up being [{spfyid: set(targets)}, spfyid: set(targets)}] with spfyids being multiple
    dicts_targets = []
    # define a list (for groups) of dictionary of targets to sets of spfyids
    # end structure is: [{gene:set(spfyids)}, {gene:set(spfyids)}] with genes being multiple
    collapsed_targets = []
    # define terms required for fishers
    queryAttributeUris = []
    # define a results list to pass to fishers.py
    results = []

    # enum through the groups and parse negations/logical operators to build a set of spfyids
    for index, group in enumerate(groups):
        sets_spfyids[index] = handle_logical(group)
        # define a blank dictionary for that spfyid
        dicts_targets[index] = {}
        for spfyid in sets_spfyids[index]:
            dicts_targets[index][spfyid] = query_targets(spfyid, target)

        # collapse/invert the results so we use targets as keys instead of spfyids
        collapsed_targets[index] = collapse(dicts_targets[index])

        # put together the results for that group
        N = len(sets_spfyids[index])
        results[index] = {}
        results[index]['N'] = N
        results[index]['d'] = collapsed_targets[index]

        # put together the term/labels for fishers
        queryAttributeUris[index] = ""
        for query in group:
            # where query is of form:
            # # d is of form: {"negated":false,"relation":"http://purl.obolibrary.org/obo/GENEPIO_0001076","attribute":"O136","logical":null}
            # negation
            if query['negated']:
                queryAttributeUris[index] += 'NOT '
            # attribute
            queryAttributeUris[index] += query['attribute'] + ' '
            # logical operator
            if len(group) > 1 and index < len(group)-1 and 'logical' in query.keys():
                queryAttributeUris[index] += query['logical'] + ' '
        queryAttributeUris[index] = queryAttributeUris[index].strip()

    df = fishers(queryAttributeUris[0], queryAttributeUris[1], target, results)
    return df

if __name__ == "__main__":
    import time
    da1 = {"negated":False,"relation":"http://purl.obolibrary.org/obo/GENEPIO_0001076","attribute":"O157",
    "logical":"OR"}
    da2 = {"negated":False,"relation":"http://purl.obolibrary.org/obo/GENEPIO_0001076","attribute":"O136"}
    da = [da1,da2]

    db1 = {"negated":False,"relation":"http://purl.obolibrary.org/obo/GENEPIO_0001076","attribute":"O84",
    "logical":"OR"}
    db2 = {"negated":False,"relation":"http://purl.obolibrary.org/obo/GENEPIO_0001076","attribute":"O54"}
    db = [db1,db2]

    target = "https://www.github.com/superphy#Marker"

    start = time.time()
    print groupcomparisons([db1,db2], target)
    stop = time.time()
    print (stop-start)
