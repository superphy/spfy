import logging
from modules.loggingFunctions import initialize_logging
from middleware.decorators import tojson, prefix, submit

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)

def _query_contigids(recordid):
    '''Retrieves a list of contigids for a given record.id
    along with basic information such as filename, serotype.
    '''
    query = """
    SELECT DISTINCT ?Genome ?submitted ?otype ?htype ?recordid ?uriContig WHERE {{
        ?uriContig a g:Contig ; g:Identifier ?recordid .
        VALUES ?recordid {{ "{}" }} .
        ?uriContig :isFoundIn ?GenomeObject .
        ?GenomeObject a g:Genome ; dc:description ?Genome; dc:date ?submitted .
        ?GenomeObject :isFoundIn ?spfyIdObject .
        ?spfyIdObject a :spfyId .
        OPTIONAL {{
            ?spfyIdObject ge:0001076 ?otype .
            ?spfyIdObject ge:0001077 ?htype .
        }}
    }}
    """.format(recordid)
    return query

@tojson
@submit
@prefix
def query_db_accession(recordid):
    '''
    Searches the graph database and finds results for a given record.id
    '''
    query = """
    SELECT DISTINCT ?Genome ?submitted ?otype ?htype ?contigid ?subclass ?marker WHERE {{
        ?uriContig a g:Contig ; g:Identifier ?recordid .
        VALUES ?recordid {{ "{}" }} .
        ?uriContig :isFoundIn ?GenomeObject .
        ?GenomeObject a g:Genome ; dc:description ?Genome; dc:date ?submitted .
        ?GenomeObject :isFoundIn ?spfyIdObject .
        ?spfyIdObject a :spfyId .
        ?spfyIdObject :hasPart ?contigs .
        ?contigs a g:Contig .
        ?contigs g:Identifier ?contigid
        OPTIONAL {{
            ?spfyIdObject ge:0001076 ?otype .
            ?spfyIdObject ge:0001077 ?htype .
        }}
        OPTIONAL {{
            ?contigs :hasPart ?marker .
            ?marker a :Marker .
            ?subclass rdfs:subClassOf :Marker .
            ?marker a ?subclass .
            FILTER (?subclass != typon:Locus && ?subclass != :Marker)
        }}
    }}
    """.format(recordid)
    return query

def _row(genome, contigid, marker, submitted, subclass=None, analysis=None):
    # If the analysis type is not supplied,
    # retrieve it from the subclass.
    if not analysis:
        analysis = subclass.split('#')[-1]

    # https://www.github.com/superphy#acrB
    hitname = marker.split('#')[-1]

    # The actual row.
    d = {
        'filename': genome,
        'contigid': contigid,
        'hitname': hitname,
        'date': submitted,
        'analysis': analysis
    }
    return d

def search_accession(recordid):
    '''The actual function submitted as an RQ job.
    Handles searching and parsing of the result for
    the front-end.
    '''

    # Retrieve the list of dictionaries of results.
    l = query_db_accession(recordid)

    if not l:
        # Query returned an empty list.
        return []

    # The return:
    ret = []
    
    # Take the first element and create a row
    # with the serotype.
    first = l[0]
    ret.append(
        _row(
            genome=first['Genome'],
            contigid='n/a',
            marker='{0}/{1}'.format(first['otype'],first['htype']),
            submitted=first['submitted'],
            analysis='Serotype'
        )
    )

    # Iterate through the results and appned rows.
    for d in l:
        ret.append(
            _row(
                genome=d['Genome'],
                contigid=d['contigid'],
                marker=d['marker'],
                submitted=d['submitted'],
                subclass=d['subclass']
            )
        )
    
    return ret
