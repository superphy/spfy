import config
import logging
import time
# import cPickle as pickle
from functools import wraps
from SPARQLWrapper import SPARQLWrapper, JSON
from modules.loggingFunctions import initialize_logging
from modules.turtleGrapher.turtle_utils import generate_uri as gu
from modules.groupComparisons.sparql_utils import generate_prefixes

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)

blazegraph_url = config.database['blazegraph_url']
#blazegraph_url = 'http://localhost:8080/bigdata/sparql'

def toset(targetname):
    '''
    A decorator to convert JSON response of sparql query to a set.
    '''
    def toset_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            results = func(*args, **kwargs)
            st = set()
            for result in results['results']['bindings']:
                st.add(result[targetname]['value'])
            log.debug(st)
            return st
        return func_wrapper
    return toset_decorator

def tolist(targetname):
    '''
    A decorator to convert JSON response of sparql query to a list.
    '''
    def tolist_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            results = func(*args, **kwargs)
            l = []
            for result in results['results']['bindings']:
                l.append(result[targetname]['value'])
            log.debug(l)
            return l
        return func_wrapper
    return tolist_decorator

def submit(func):
    '''
    A decorator to submit a given query generation function.
    '''
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        query = func(*args, **kwargs)
        sparql = SPARQLWrapper(blazegraph_url)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results
    return func_wrapper

@tolist(targetname='objectinstance')
@submit
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
    query = """
    SELECT DISTINCT ?objectinstance WHERE {{
        ?objectinstance a <{objectTypeUri}> .
    }}
    """.format(objectTypeUri=objectTypeUri)
    return query

@tolist(targetname='attributetype')
@submit
def get_all_attribute_types():
    '''
    Returns all types of attributes (ie. all edge types) currently in blazegraph.
    '''
    # SPARQL Query
    query = """
    SELECT DISTINCT ?attributetype WHERE {{
        ?anything ?attributetype ?attribute .
    }}
    """
    return query

@tolist(targetname='attribute')
@submit
def get_attribute_values(attributeTypeUri):
    '''
    Given an attribute type(ex. ge:0001076, aka. O-Type).
    Returns a list of all distinct attribute values.
    '''
    # SPARQL Query
    query = """
    SELECT DISTINCT ?attribute WHERE {{
        ?s <{attributeTypeUri}> ?attribute .
    }}
    """.format(attributeTypeUri=attributeTypeUri)
    return query

@toset(targetname='objecttype')
@submit
def get_types():
    '''
    Gets a list distinct rdf:type objects (ie. all possible object types) by querying the blazegraph db.
    Used to determine if a given query Uri is an object type or an attribute of the object.
    Returns just the URIs.
    '''
    # SPARQL Query
    query = """
    SELECT DISTINCT ?objecttype WHERE {{
        ?objectinstance a ?objecttype .
    }}
    """
    return query

def is_group(uri):
    '''
    Returns True if a given URI is in the list of possible object types (ie. group types), otherwise False (ie. attributeType).
    '''
    log.debug(uri)
    isgroup = unicode(uri) in get_types()
    log.debug(isgroup)
    return isgroup

def parse_results_todict(results, subjectname, targetname):
    '''
    Converts SPARQL JSON results into a python dictionary.
    We reverse the order as we're more interested in targetname: count(DISTINCT subjectname).
    The use of sets is to ensure DISTINCT (though this should be accounted for by SPARQL query).
    '''
    # this is the general dict to hold results
    d = {}
    # a set to count number of unique subjectnames
    st = set()
    # the loop
    for result in results['results']['bindings']:
        if result[targetname]['value'] in d.keys():
            # then a set already exists
            d[result[targetname]['value']].add(result[subjectname]['value'])
        else:
            d[result[targetname]['value']] = set([result[subjectname]['value']])
        # add the subjectname to the set
        st.add(result[subjectname]['value'])
    # temp code to pickle result
    # pickle.dump(d,open(str(time.time()) + '.p', 'wb'))
    return {'n':len(st),'d':d}

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
    return parse_results_todict(results, 's', 'target')

def query(queryAttributeUriA, queryAttributeUriB, targetUri, queryAttributeTypeUriA='?p', queryAttributeTypeUriB='?p'):
    # base dictionary for results
    d = {}

    # query results for UriA
    resultsA = to_target(queryAttributeUriA, targetUri, queryAttributeTypeUriA)
    log.debug(resultsA)
    d.update({'A':resultsA})

    # query results for UriB
    resultsB = to_target(queryAttributeUriB, targetUri, queryAttributeTypeUriB)
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
    log.info(get_all_attribute_types())
    # user selects an attribute type => get all distinct attribute values
    log.info(get_attribute_values(gu('ge:0001076')))
    # user selects two specific values
    # at this point, we no longer have to worry about query speed because none of the below queries are immediately returned to the ui (instead, they are handled in RQ)
    start = time.time()
    log.info(start)
    log.info(query('O157', 'O101', gu(':VirulenceFactor'), gu('ge:0001076'), gu('ge:0001076')))
    stop = time.time()
    log.info(stop-start)
