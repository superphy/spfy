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
    SELECT DISTINCT ?Genome ?submitted ?otype ?htype ?recordid ?subclass ?marker WHERE {{
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
        OPTIONAL {{
            ?uriContig :hasPart ?marker .
            ?marker a :Marker .
            ?subclass rdfs:subClassOf :Marker .
            ?marker a ?subclass .
            FILTER (?type == "http://purl.phyloviz.net/ontology/typon#Locus" || ?type == "https://www.github.com/superphy#Marker")
        }}
    }}
    """.format(recordid)
    return query
