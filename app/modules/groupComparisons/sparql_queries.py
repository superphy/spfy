import config
import logging
from SPARQLWrapper import SPARQLWrapper, JSON
from modules.loggingFunctions import initialize_logging
from modules.turtleGrapher.turtle_utils import generate_uri as gu
from modules.groupComparisons.sparql_utils import generate_prefixes

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)

#blazegraph_url = config.database['blazegraph_url']
blazegraph_url = 'http://localhost:8080/bigdata/sparql'

def get_all_atribute_types():
    '''
    Returns all types of attributes (ie. all edge types) currently in blazegraph.
    '''
    # SPARQL Query
    sparql = SPARQLWrapper(blazegraph_url)
    query = """
    SELECT DISTINCT ?attributetype WHERE {{
        ?anything ?attributetype ?attribute .
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return parse_results(results, 'attributetype', objectTypeUri)

def get_attribute_values(objectTypeUri, attributeTypeUri):
    '''
    Given an objectype(ex. :spfyId) and an attribute type(ex. so:0001076, aka. O-Type).
    Returns a list of all distinct attribute values associated with those two conditions.
    '''
    # SPARQL Query
    sparql = SPARQLWrapper(blazegraph_url)
    query = """
    SELECT DISTINCT ?attribute WHERE {{
        ?s a <{objectTypeUri}> ; <{attributeTypeUri}> ?attribute .
    }}
    """.format(objectTypeUri=objectTypeUri, attributeTypeUri=attributeTypeUri)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    log.debug(results)
    return parse_results(results, 'attribute', attributeTypeUri)

def get_attribute_types(objectTypeUri):
    '''
    Given a object type uri, returns a simple list of all distinct attribute types it has.
    '''
    # SPARQL Query
    sparql = SPARQLWrapper(blazegraph_url)
    query = """
    SELECT DISTINCT ?attributetype WHERE {{
        ?s a <{objectTypeUri}> ; ?attributetype ?attribute .
    }}
    """.format(objectTypeUri=objectTypeUri)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    log.debug(results)
    return parse_results(results, 'attributetype', objectTypeUri)

def get_instances(objectTypeUri):
    '''
    Gets all instances of a given object type.
    Example use: to get all :Markers in blazegraph.
    Args:
        objecttype: a rdflib.URI
    Returns:
        a list of the result.
    '''
    # SPARQL Query
    sparql = SPARQLWrapper(blazegraph_url)
    query = """
    SELECT DISTINCT ?objectinstance WHERE {{
        ?objectinstance a <{objectTypeUri}> .
    }}
    """.format(objectTypeUri=objectTypeUri)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return parse_results(results, 'objectinstance', objectTypeUri)

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
    log.debug(tup)
    return tup

def is_group(uri):
    '''
    Returns True if a given URI is in the list of possible object types (ie. group types), otherwise False.
    '''
    isgroup = uri in get_types()
    log.debug(isgroup)
    return isgroup

def parse_results(results, targetname, queryUri):
    '''
    Used to fix structure of SPARQL query results for running group comparisons.
    '''
    l = []
    for result in results['results']['bindings']:
        l.append(result[targetname]['value'])
    log.debug(l)
    return {queryUri: l}

def to_target(queryUri, targetUri):
    '''
    Generates a query that selects all targetUri from groupUri
    '''
    sparql = SPARQLWrapper(blazegraph_url)
    # add PREFIXes to sparql query
    query = generate_prefixes()
    # the queries have to be structured differently if the queryUri is a object type or is a specific instance
    if is_group(queryUri):
        # then queryUri is a object type
        query += """
        SELECT ?target WHERE {{
            ?spfyid a <{queryUri}> ; (:hasPart|:isFoundIn) ?target .
            ?target a <{targetUri}> .
        }}
        """.format(queryUri=queryUri, targetUri=targetUri)
    else:
        # then queryUri is a specific object
        query += """
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
    # base dictionary for results
    d = {}

    # query results for UriA
    resultsA = to_target(queryUriA, targetUri)
    log.debug(resultsA)
    d.update(resultsA)

    # query results for UriB
    resultsB = to_target(queryUriB, targetUri)
    log.debug(resultsB)
    d.update(resultsB)

    return d

if __name__ == "__main__":
    '''
    For testing...
    '''
    print log_file
    #print query(gu(':spfy1'),gu(':spfy2'),gu(':Marker'))
    log.debug(get_types())
    log.debug(get_instances(gu(':spfyId')))
    log.debug(get_attribute_types(gu(':spfyId')))
    log.debug(get_attribute_values(gu(':spfyId'), gu('so:0001076')))
