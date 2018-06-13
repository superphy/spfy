import logging
from modules.loggingFunctions import initialize_logging
from middleware.decorators import tojson, prefix, submit

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)

@tojson
@submit
@prefix
def query_db_file(s):
    '''
    Searches the graph database and finds results for a given filename.
    Args:
        s(str) the name of a genome file.
    '''
    query = """
    SELECT DISTINCT ?Genome ?submitted ?otype ?htype ?contig ?vf ?amr WHERE {{
        ?GenomeObject a g:Genome ; dc:description ?Genome; dc:date ?submitted .
        VALUES ?Genome {{ {} }}
        ?spfyIdObject (:hasPart|:isFoundIn) ?GenomeObject .
        ?GenomeObject :hasPart ?contig.
        ?contig a g:Contig .
        OPTIONAL {
            ?spfyIdObject ge:0001076 ?otype .
            ?spfyIdObject ge:0001077 ?htype .
            ?contig :hasPart ?vf.
            ?vf a :VirulenceFactor.
            ?contig :hasPart ?amr.
            ?amr a :AntimicrobialResistanceGene.
        }
    }}
    """.format(s)
    return query
