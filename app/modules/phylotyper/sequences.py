"""Classes for retrieving Marker sequences


Example:
    $ python sequences.py -s stx1

"""

from modules.decorators import submit, prefix, tojson
from modules.turtleGrapher import turtle_utils

@submit
@prefix
def marker_query(marker_uris):

  query = '''
  SELECT ?m 
  WHERE {{
    ?m rdf:type :Marker .
    VALUES ?m {{ {} }}
  }}
  '''.format(' '.join(marker_uris))

  return query

@tojson
@submit
@prefix
def sequence_query(marker_rdf, genome_rdf):

    query = '''
        SELECT ?contig ?region ?start ?len ?seq
        WHERE {{
            ?g a g:Genome .
            VALUES ?g {{ {} }}
            ?contig a g:Contig .
            ?m a :VirulenceFactor .
            ?contig g:DNASequence ?dna .
            VALUES ?m {{ {} }} .
            ?region a faldo:Region ;
                :hasPart ?m ;
                :isFoundIn ?contig ;
                :isFoundIn ?g ;
                faldo:begin ?b ;
                faldo:end ?e .
            ?b faldo:position ?beginPos .
            ?e faldo:position ?endPos .
            BIND( IF(?beginPos < ?endPos,?beginPos,?endPos) as ?start) 
            BIND( IF(?beginPos < ?endPos,?endPos-?beginPos+1,?beginPos-?endPos+1) as ?len) 
            BIND( SUBSTR( ?dna, ?start, ?len ) as ?seq )
        }}
    '''.format(genome_rdf, ' '.join(marker_rdf))

    return query



class MarkerSequences(object):
    """Retrieve DNA region sequences for one or more Markers

    """

    def __init__(self, markers=[':stx2A',':stx2B']):
        """Constructor

        Args:


        """

        # convert to proper RDF terms
        self.marker_uris = [turtle_utils.normalize_rdfterm(m) for m in markers]
        

    def sequences(self, genome_uri):
        """Retrieve sequences for object alleles

          Args:
            genome_uri(str): Genome URI

          Returns:
            dictionary

        """

        genome_rdf = turtle_utils.normalize_rdfterm(genome_uri)
        query_result = sequence_query(self.marker_uris, genome_rdf)

        # Unroll result into dictionary with fasta-like keys
        seqdict = { "spfy|{}| {}:{}..{}".format(
            turtle_utils.fulluri_to_basename(r['region']), 
            turtle_utils.fulluri_to_basename(r['contig']), r['start'], r['start']+r['len']-1): r['seq'] for r in query_result }

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
