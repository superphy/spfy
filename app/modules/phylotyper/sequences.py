"""Classes for retrieving Marker sequences


Example:
    $ python sequences.py -s stx1

"""
import os
from rdflib import Graph
from middleware.decorators import submit, prefix, tojson
from middleware.graphers import turtle_utils
from routes.job_utils import fetch_job
from modules.phylotyper.ontology import stx1_graph, stx2_graph, eae_graph, LOCI
from middleware.graphers.turtle_utils import generate_uri as gu

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

@prefix
def sequence_query(marker_rdf, isolate_rdf):
    # query = '''
    #         SELECT ?contig ?contigid ?region ?start ?len ?seq
    #         WHERE {{
    #             ?g a :spfyId .
    #             VALUES ?g {{ {} }}
    #             ?contig a g:Contig ;
    #                 g:Identifier ?contigid .
    #             ?m a :VirulenceFactor .
    #             ?contig g:DNASequence ?dna .
    #             VALUES ?m {{ {} }} .
    #             ?region a faldo:Region ;
    #                 :hasPart ?m ;
    #                 :isFoundIn ?contig ;
    #                 :isFoundIn ?g ;
    #                 faldo:begin ?b ;
    #                 faldo:end ?e .
    #             ?b faldo:position ?beginPos .
    #             ?e faldo:position ?endPos .
    #             BIND( IF(?beginPos < ?endPos,?beginPos,?endPos) as ?start)
    #             BIND( IF(?beginPos < ?endPos,?endPos-?beginPos+1,?beginPos-?endPos+1) as ?len)
    #             BIND( SUBSTR( ?dna, ?start, ?len ) as ?seq )
    #         }}
    #     '''.format(isolate_rdf, ' '.join(marker_rdf))

    query = '''
            SELECT ?contig ?contigid ?region ?start ?len ?seq
            WHERE {{
                ?g a :spfyId .
                VALUES ?g {{ {} }}
                ?contig a g:Contig ;
                    g:Identifier ?contigid .
                ?m a :VirulenceFactor .
                ?contig g:DNASequence ?dna .
                VALUES ?m {{ {} }} .
                ?region a faldo:Region ;
                    :hasPart ?m ;
                    faldo:begin ?b ;
                    faldo:end ?e .
                ?b faldo:position ?beginPos .
                ?e faldo:position ?endPos .
                ?region :isFoundIn ?contig .
                ?contig :isFoundIn ?bagOfContigs .
                ?bagOfContigs :isFoundIn ?genomeHash .
                ?genomeHash :isFoundIn ?g .
                BIND( IF(?beginPos < ?endPos,?beginPos,?endPos) as ?start)
                BIND( IF(?beginPos < ?endPos,?endPos-?beginPos+1,?beginPos-?endPos+1) as ?len)
                BIND( SUBSTR( ?dna, ?start, ?len ) as ?seq )
            }}
        '''.format(isolate_rdf, ' '.join(marker_rdf))

    return query


@tojson
@submit
@prefix
def phylotyper_query(subtypescheme_rdf, isolate_rdf):

    query = '''

        SELECT DISTINCT ?pt ?typeLabel ?score ?region ?contigid ?beginPos ?endPos
        WHERE {{
            ?pt a subt:PTST ;
                subt:isOfPhylotyper {} ;
                subt:hasIdentifiedClass ?type ;
                subt:score ?score ;
                typon:hasIdentifiedAllele ?a .
            ?type subt:subtypeValue ?typeLabel .
            ?a faldo:location ?region .
            ?region :isFoundIn {} ;
                :isFoundIn ?contig ;
                faldo:begin ?b ;
                faldo:end ?e .
            ?contig a g:Contig ;
                g:Identifier ?contigid .
            ?b faldo:position ?beginPos .
            ?e faldo:position ?endPos
        }}
    '''.format(subtypescheme_rdf, isolate_rdf)

    return query


@tojson
@submit
@prefix
def genename_query(locus_rdf):

    query = '''
        SELECT ?markerURI ?markerLabel
        WHERE {{
            VALUES ?l {{ {} }} .
            ?markerURI :isFoundIn ?l ;
                a :Marker ;
                dc:description ?markerLabel
        }}
    '''.format(locus_rdf)

    return query



class MarkerSequences(object):
    """Retrieve DNA region sequences for one or more Markers

    """

    def __init__(self, markers=[':stx2A',':stx2B'], job_id=None, job_turtle=None, job_ectyper_datastruct_vf=None, redis_conn=None):
        """Constructor

        Args:


        """

        # convert to proper RDF terms
        self.marker_uris = [turtle_utils.normalize_rdfterm(m) for m in markers]
        # Read the phylotyper ontology as a starter graph.
        g = Graph()
        ontology_turtle_file = os.path.join(__location__, 'superphy_subtyping.ttl')
        g.parse(ontology_turtle_file, format="turtle")
        # Add Phylotyper ontology graphs.
        g = g + stx1_graph() + stx2_graph() + eae_graph()
        # Retrieve and merge graphs from pre-req. jobs.
        self.graph = g + fetch_job(job_id, redis_conn).result +  fetch_job(job_turtle, redis_conn).result + fetch_job(job_ectyper_datastruct_vf, redis_conn).result

    def sequences(self, genome_uri):
        """Retrieve sequences for object alleles

          Args:
            genome_uri(str): Genome URI

          Returns:
            dictionary

        """
        #raise Exception('graph: {0}'.format(self.graph.serialize(format="turtle")))
        genome_rdf = turtle_utils.normalize_rdfterm(genome_uri)
        query = sequence_query(self.marker_uris, genome_rdf)
        # query_result = sequence_query(self.marker_uris, genome_rdf)
        query_result = self.graph.query(query)
        # ?contig ?contigid ?region ?start ?len ?seq
        l = [
            {
                'contig': str(tup[0].toPython()),
                'contigid': str(tup[1].toPython()),
                'region': str(tup[2].toPython()),
                'start': int(tup[3].toPython()),
                'len': int(tup[4].toPython()),
                'seq': str(tup[5].toPython())
            }
            for tup in query_result
        ]

        # Unroll result into dictionary with fasta-like keys
        seqdict = { "spfy|{}| {}:{}..{}".format(
            turtle_utils.fulluri_to_basename(r['region']),
            r['contigid'], r['start'], r['start']+r['len']-1): r['seq'] for r in l }

        return seqdict


    def fasta(self, genome_uri):
        """Retrieve sequences for object alleles

          Args:
            genome_uri(str): Genome URI

          Returns:
             fasta format string or None

        """

        seqdict = self.sequences(genome_uri)

        if not seqdict:
            return None

        fasta_string = ''
        for (h,s) in seqdict.iteritems():
            fasta_string += ">{}\n{}\n".format(h,s)

        return fasta_string

    @prefix
    def _subtype_query(self):
        """
        Queries for a specific URI of given type

        Returns:
            dictionary

        """
        query = '''
            SELECT ?subtype
            WHERE {{
                ?region a faldo:Region ; :hasPart ?subtype .
                ?subtype a :VirulenceFactor .
            }}
            '''

        return query

    def _find_object(self, uri):
        """
        Returns true if URI is already in database

        Args:
            uri(str): URI with prefix defined in config.py
            rdftype(str): the URI linked by a rdf:type relationship to URI

        """

        query = self._subtype_query()

        query_result = self.graph.query(query)

        l = [tup[0].toPython() for tup in query_result]
        full_uri = str(gu(uri))

        return full_uri in l

    def validate(self, subtype):
        """Checks that the MakerSequence.graph has all the alleles required
        for phylotyper analysis. Returns False if not (& Phylotyper should
        not be run).
        """
        # Check for existance of schema Marker components
        for l in LOCI[subtype]:
            if not self._find_object(l):
                return False
        return True

if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        nargs="*",
        help="Marker URI",
        required=True
    )
    parser.add_argument(
        "-g",
        help="Genome URI",
        required=True
    )
    args = parser.parse_args()

    ms = MarkerSequences(args.m)
    print ms.sequences(args.g)
