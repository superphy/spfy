from handle_logical import handle_logical, query_targets

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
    # defin a list (for groups) of dictionary of targets to sets of spfyids
    # end structure is: [{gene:set(spfyids)}, {gene:set(spfyids)}] with genes being multiple
    collapsed_targets = []
    # enum through the groups and parse negations/logical operators to build a set of spfyids
    for index, group in enumerate(groups):
        sets_spfyids[index] = handle_logical(group)
        # define a blank dictionary for that spfyid
        dicts_targets[index] = {}
        for spfyid in sets_spfyids[index]:
            dicts_targets[index][spfyid] = query_targets(spfyid, target)

        # collapse the results
        collapsed_targets[index] = collapse(dicts_targets[index])
