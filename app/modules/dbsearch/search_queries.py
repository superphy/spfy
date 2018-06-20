import logging
from modules.loggingFunctions import initialize_logging
from middleware.decorators import tojson, prefix, submit

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)

@tojson
@submit
@prefix
def query_db_accession(recordid):
    '''
    Searches the graph database and finds results for a given record.id
    '''
    query = """
    SELECT DISTINCT ?Genome ?submitted ?otype ?htype ?recordid ?vf ?amr WHERE {{
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
            ?uriContig :hasPart ?vf.
            ?vf a :VirulenceFactor .
        }}
        OPTIONAL {{
            ?uriContig :hasPart ?amr.
            ?amr a :AntimicrobialResistanceGene .
        }}
    }}
    """.format(recordid)
    return query
