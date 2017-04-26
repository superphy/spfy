import config
import logging
import time
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

    return parse_results_tolist(results, 'attributetype')

def get_attribute_values(attributeTypeUri):
    '''
    Given an attribute type(ex. ge:0001076, aka. O-Type).
    Returns a list of all distinct attribute values.
    '''
    # SPARQL Query
    sparql = SPARQLWrapper(blazegraph_url)
    query = """
    SELECT DISTINCT ?attribute WHERE {{
        ?s <{attributeTypeUri}> ?attribute .
    }}
    """.format(attributeTypeUri=attributeTypeUri)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    log.debug(results)
    return parse_results_tolist(results, 'attribute')

def get_types():
    '''
    Gets a list distinct rdf:type objects (ie. all possible object types) by querying the blazegraph db.
    Used to determine if a given query Uri is an object type or an attribute of the object.
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
    Returns True if a given URI is in the list of possible object types (ie. group types), otherwise False (ie. attributeType).
    '''
    isgroup = uri in get_types()
    log.debug(isgroup)
    return isgroup

def parse_results_tolist(results, targetname):
    '''
    Used to a simple list SPARQL query results for running group comparisons.
    '''
    l = []
    for result in results['results']['bindings']:
        l.append(result[targetname]['value'])
    log.debug(l)
    return l

def to_target(attributeUri, targetUri, attributeTypeUri='?p'):
    '''
    Generates a query that selects all targetUri from a given attribute group.
    The attributeTypeUri isn't necessary, but specifying it (instead of using the wildcard) improves performance.
    '''
    sparql = SPARQLWrapper(blazegraph_url)
    # add PREFIXes to sparql query
    query = generate_prefixes()
    # the queries have to be structured differently if the queryUri is a object type or is a specific instance
    if is_group(targetUri):
        # then targetUri is a object type
        query += """
        SELECT ?s ?target WHERE {{
            ?s <{attributeTypeUri}> '{attributeUri}' ; (:hasPart|:isFoundIn) ?target .
            ?target a <{targetUri}> .
        }}
        """.format(attributeTypeUri=attributeTypeUri, attributeUri=attributeUri, targetUri=targetUri)
    else:
        # then targetUri is an attribute
        query += """
        SELECT ?s ?target WHERE {{
            ?s <{attributeTypeUri}> '{attributeUri}' ; (:hasPart|:isFoundIn) ?targetobject .
            ?targetobject <{targetUri}> ?target.
        }}
        """.format(attributeTypeUri=attributeTypeUri, attributeUri=attributeUri, targetUri=targetUri)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def query(queryAttibuteUriA, queryAttibuteUriB, targetUri, queryAttributeTypeUriA='?p', queryAttributeTypeUriB='?p'):
    # base dictionary for results
    d = {}

    # query results for UriA
    resultsA = to_target(queryAttibuteUriA, targetUri, queryAttributeTypeUriA)
    log.debug(resultsA)
    d.update({'A':resultsA})

    # query results for UriB
    resultsB = to_target(queryAttibuteUriB, targetUri, queryAttributeTypeUriB)
    log.debug(resultsB)
    d.update({'B':resultsB})

    return d

if __name__ == "__main__":
    '''
    For testing...
    '''
    print log_file
    #print query(gu(':spfy1'),gu(':spfy2'),gu(':Marker'))
    # get all possible attribute types
    log.info(get_all_atribute_types())
    # user selects an attribute type => get all distinct attribute values
    log.info(get_attribute_values(gu('ge:0001076')))
    # user selects two specific values
    # at this point, we no longer have to worry about query speed because none of the below queries are immediately returned to the ui (instead, they are handled in RQ)
    log.info(is_group(':Marker'))
    log.info(is_group(unicode(':VirulenceFactor')))
    log.info(is_group(':ECP'))
    start = time.time()
    log.info(start)
    log.info(query('O157', 'O101', gu(':VirulenceFactor'), gu('ge:0001076'), gu('ge:0001076')))
    stop = time.time()
    log.info(stop-start)
