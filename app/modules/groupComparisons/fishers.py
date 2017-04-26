import scipy.stats as stats
import pandas as pd
from modules.turtleGrapher.turtle_utils import generate_uri as gu
from modules.groupComparisons.sparql_queries import query, get_instances

def fishers(queryAttibuteUriA, queryAttibuteUriB, targetUri, queryAttributeTypeUriA='?p', queryAttributeTypeUriB='?p'):
    # query the blazegraph db for results
    results = query(queryAttibuteUriA, queryAttibuteUriB, targetUri, queryAttributeTypeUriA, queryAttributeTypeUriB)
    # split the results into sub vars
    ## num of uniq subjects in A
    nA = results['A']['n']
    ## num of uniq subjects in B
    nB = results['B']['n']
    ## dictionary with the results from A
    dictA = results['A']['d']
    ## dictionary with the results from B
    dictB = results['B']['d']

    # join all possible targets as req for Fisher's
    # we could instead query the db for `DISTINCT ?s WHERE ?s a targetUri`, but I'm not interested in targets that neither queryA nor queryB has.
    all_targets = set(dictA.keys())
    all_targets.add(dictB.keys())

    # create a pandas dataframe for storing aggregate results from fisher's
    df = pd.DataFrame(columns=['target','queryA','queryB','presentQueryA','absentQueryA','presentQueryB','absentQueryB','pvalue','oddsratio'])

    # iterate through targets and perform fisher's
    for index, target in enumerate(all_targets):
        # tags for dataframe
        queryA = queryAttibuteUriA
        queryB = queryAttibuteUriB
        # check if target is found in queryA
        if target in dictA.keys():
            presentQueryA = len(dictA[target])
        else:
            presentQueryA = 0
        absentQueryA = nA - presentQueryA
        # check if target is found in queryB
        if target in dictB.keys():
            presentQueryB = len(dictB[target])
        else:
            presentQueryB = 0
        absentQueryB = nB - presentQueryB
        # compute fisher's exact test
        # table structure is:
        #           queryUriA   queryUriB
        #   Present
        #   Absent
        pvalue, oddsratio = stats.fisher_exact([[presentQueryA, presentQueryB], [absentQueryA, absentQueryB]])
        # add results to new row on pandas dataframe
        df.loc[index] = [target,queryA,queryB,presentQueryA,absentQueryA,presentQueryB,absentQueryB,pvalue,oddsratio]

    return df

if __name__ == "__main__":
    '''
    For testing...
    '''
    print fishers('O157', 'O101', gu(':VirulenceFactor'), gu('ge:0001076'), gu('ge:0001076'))
