import config  # this is the config.py
from rdflib import Namespace, URIRef, Literal

def generate_hash(filename):
    from hashlib import sha1
    # the 'b' isn't needed less you run this on Windows
    with open(filename, 'rb') as f:
        # we apply a sort func to make sure the contents are the same,
        # regardless of order
        return sha1(str(sorted(f.readlines()))).hexdigest()

def slugify(value):
    """
    from Django
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    import re
    value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s\/\./:-]', '', value).strip())
    value = unicode(re.sub('[-\s]+', '-', value))
    return value

def generate_uri(uri, s=''):
    """
    Takes a string as one would define for .ttl files and returns a URI for rdflib.

    Args:
        uri (str): a string following .ttl convention for a URI
        ex. g:Identifier as shorthand for http://www.biointerchange.org/gfvo#Identifier
    Returns:
        (rdflib.URIRef) with URI needed to add to rdflib.Graph
    """

    # if you call with a uri already
    if isinstance(uri, URIRef):
        s = slugify(s)
        return URIRef(str(uri) + s)
    elif type(uri) is str and bool(urlparse.urlparse(uri).scheme):
        # if you called with a string in the form of a valid url
        return URIRef(uri)
        
    prefix = uri.split(':')[0]
    postfix = uri.split(':')[1]

    postfix = slugify(postfix)

    if prefix == '':  # this is our : case
        return URIRef(config.namespaces['root'] + postfix)
    else:
        return URIRef(config.namespaces[prefix] + postfix)


def uri_to_basename(uri):
    '''
    This does the reverse of generate_uri(). Converts a rdflib.term.URIRef back to is base.
        ex. rdflib.term.URIRef(u'https://www.github.com/superphy#4eb02f5676bc808f86c0f014bbce15775adf06ba)
                gives 4eb02f5676bc808f86c0f014bbce15775adf06ba
    Args:
        uri(rdflib.term.URIRef): a URIRef object
    Returns:
        (str): just the basestring (ie. everything after the : in rdf syntax)
    '''

    for value in config.namespaces.keys():
        if value in uri:
            return str(uri).strip(value)
    # if the clean method above fails, default to '/' splitting
    # this will fail if a path-style uri is used
    return str(uri).split('/')[-1]

def link_uris(graph, uri_towards_spfyid, uri_towards_marker):
    '''
    Links two vertices in a graph as required for inferencing/queries in blazegraph.
    Blazegraph has problems (hangs after 3-4 uploads) with owl:SymmetricProperty, so we use :hasPart which we apply owl:TransitiveProperty to link everything in :spfyId -> :Marker and use :isFoundIn (same owl:TransitiveProperty) to link everything :Marker -> :spfyId
    This means that you can't just query a vertex type and look for another vertex type -> you must know the direction you're moving in (think subway trains). We accomadate this by defining a dictionary that maps object types to a given numerical weight so we can do a comparison of weights to determine direction.
    The owl:TransitiveProperty is defined in generate_graph() under turtle_grapher.py
    '''
    graph.add((uri_towards_spfyid, generate_uri(':hasPart'), uri_towards_marker))
    graph.add((uri_towards_marker, generate_uri(':isFoundIn'), uri_towards_spfyid))
    return graph
