import config
from modules.groupComparisons.ontology_weight import weights

blazegraph_url = config.database['blazegraph_url']

def get_type(uri):
    '''
    Gets the object type of a given uri by querying the blazegraph db.
    '''
    pass

def to_target(groupUri, targetUri):
    '''
    Generates a query that selects all targetUri from groupUri
    '''
    pass

def query(groupUriA, groupUriB, targetUri):
    sparql = SPARQLWrapper(blazegraph_url)

    # comparing groups
    if (groupUriA in weights.keys) and (groupUriB in weights.keys):
        # determine weights of group uris
        groupUriA_weight = weights[groupUriA]
        groupUriB_weight = weights[groupUriB]
        # use weights to determine which edge type to use in query
        if groupUriA_weight < groupUriB_weight:
            edge = gu(':hasPart')
        elif groupUriA_weight > groupUriB_weight:
            edge = gu(':isFoundIn')
        else:
            edge = 'o shihzu'

        query = """
        SELECT ?spfyid WHERE {{
            ?spfyid a <{spfyIdType}> .
            ?spfyid <{hasPart}> <{uriGenome}> .
        }}
        """.format(spfyIdType=gu(':spfyId'), hasPart=gu(':hasPart'), uriGenome=uriGenome)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
