import config
from modules.groupComparisons.ontology_weights import weights
from SPARQLWrapper import SPARQLWrapper, JSON

#blazegraph_url = config.database['blazegraph_url']
blazegraph_url = 'http://localhost:8080/bigdata/sparql'

def get_types():
    '''
    Gets a list distinct rdf:type objects (ie. all possible object types) by querying the blazegraph db.
    Used to determine if a given query Uri is an object type or a specific instance of an object.
    '''
    query = """
    SELECT DISTINCT ?objecttype WHERE {{
        ?objectinstance a ?objecttype .
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def to_target(groupUri, targetUri):
    '''
    Generates a query that selects all targetUri from groupUri
    '''
    sparql = SPARQLWrapper(blazegraph_url)
    query = """
    SELECT ?spfyid WHERE {{
        ?spfyid a <{spfyIdType}> .
        ?spfyid <{hasPart}> <{uriGenome}> .
    }}
    """.format(spfyIdType=gu(':spfyId'), hasPart=gu(':hasPart'), uriGenome=uriGenome)

def query(groupUriA, groupUriB, targetUri):
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

    sparql = SPARQLWrapper(blazegraph_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

def compare_markers(uriA, uriB):
    pass

if __name__ == "__main__":
    '''
    For testing...
    '''
    print get_types()
