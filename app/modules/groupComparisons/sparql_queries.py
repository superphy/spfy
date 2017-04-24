import config
from SPARQLWrapper import SPARQLWrapper, JSON

#blazegraph_url = config.database['blazegraph_url']
blazegraph_url = 'http://localhost:8080/bigdata/sparql'

def get_types():
    '''
    Gets a list distinct rdf:type objects (ie. all possible object types) by querying the blazegraph db.
    Used to determine if a given query Uri is an object type or a specific instance of an object.
    Parses the list and returns a tuple of just the URIs.
    '''
    # SPARQL Query
    sparql = SPARQLWrapper(blazegraph_url)
    query = """
    SELECT DISTINCT ?objecttype WHERE {{
        ?objectinstance a ?objecttype .
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    # Parse results and give me a tuple
    tup = ()
    for result in results['results']['bindings']:
        tup += (result['objecttype']['value'],)
    return tup

def is_group(uri):
    '''
    Returns True if a given URI is in the list of possible object types (ie. group types), otherwise False.
    '''
    return uri in get_types()

def parse_results(results, targetname, queryUri):
    '''
    Used to fix structure of SPARQL query results for running group comparisons.
    '''
    l = []
    for result in results['results']['bindings']:
        l.append(result[targetname]['value'])
    return {queryUri: l}

def to_target(queryUri, targetUri):
    '''
    Generates a query that selects all targetUri from groupUri
    '''
    sparql = SPARQLWrapper(blazegraph_url)
    # the queries have to be structured differently if the queryUri is a object type or is a specific instance
    if is_group(queryUri):
        # then queryUri is a object type
        query = """
        SELECT ?target WHERE {{
            ?spfyid a <{queryUri}> ; (:hasPart|:isFoundIn) ?target .
            ?target a <{targetUri}> .
        }}
        """.format(queryUri=queryUri, targetUri=targetUri)
    else:
        # then queryUri is a specific object
        query = """
        SELECT ?target WHERE {{
            <{queryUri}> (:hasPart|:isFoundIn) ?target .
            ?target a <{targetUri}> .
        }}
        """.format(queryUri=queryUri, targetUri=targetUri)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return parse_results(results, 'target', queryUri)

def query(queryUriA, queryUriB, targetUri):
    resultsA = to_target(queryUriA, targetUri)
    resultsB = to_target(queryUriB, targetUri)

if __name__ == "__main__":
    '''
    For testing...
    '''
    print get_types()
