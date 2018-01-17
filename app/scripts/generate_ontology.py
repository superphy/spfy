# baseURI: https://www.github.com/superphy#
from datetime import datetime
from rdflib import Literal
from modules.turtleGrapher.turtle_grapher import generate_graph
from modules.turtleGrapher.turtle_utils import generate_uri as gu, link_uris
from modules.blazeUploader.reserve_id import reservation_triple

def generate_ontology(example=True):
    '''
    Generates an ontology for the Spfy backend using utility methods used in
    production. Serializes the ontology as a turtle file, similar to faldo.ttl
    Recall that an ontology is really just a set of triples, but applied to
    classes/subclasses instead of specific instances.
    '''
    def write_graph(graph):
        '''
        Used to write a rdf graph to disk as a turtle file.
        '''
        data = graph.serialize(format="turtle")
        f = 'spfy_ontology.ttl'
        with open(f, 'w') as fl:
            fl.write(data)
        return f
    # generates the base graph with namespaces appended to it
    # also defines edge relations for :hasPart and :isFoundIn
    # also defines subclasses for our custom types
    graph = generate_graph()

    # adds info about this ontology being generated
    graph.add((gu('https://www.github.com/superphy#'), gu('rdf:type'), gu('owl:Ontology')))
    graph.add((gu('https://www.github.com/superphy#'), gu('dc:license'), gu('https://www.apache.org/licenses/LICENSE-2.0')))

    # spfyId class
    graph.add((gu(':spfyId'), gu('rdf:type'), gu('owl:Class')))
    graph.add((gu(':spfyId'), gu('rdfs:comment'), Literal(':spfyid')))
    # example
    if example:
        spfyid = 1
        uriGenome = gu(':de9f2c7fd25e1b3afad3e85a0bd17d9b100db4b3')
        # reservation_triple() will also link the spfyid to the genome uri.
        graph = reservation_triple(graph, uriGenome, spfyid)
        graph.add((
            gu(':spfy1'),
            gu('ge:0001567'),
            Literal('bacterium')
        ))
        graph.add((
            gu(':spfy1'),
            gu('ge:0001076'),
            Literal('O157')
        ))
        graph.add((
            gu(':spfy1'),
            gu('ge:0001076'),
            Literal('H7')
        ))
        graph.add((
            gu(':spfy1'),
            gu('ge:0001684'),
            Literal('K3')
        ))

    # ge:0001567 'bacterium'
    graph.add((gu('ge:0001567'), gu('rdf:type'), gu('owl:ObjectProperty')))
    graph.add((gu('ge:0001567'), gu('rdfs:comment'), Literal('subject species')))
    graph.add((gu('ge:0001567'), gu('rdfs:range'), gu(':spfyId')))

    # ge:0001076
    graph.add((gu('ge:0001076'), gu('rdf:type'), gu('owl:ObjectProperty')))
    graph.add((gu('ge:0001076'), gu('rdfs:comment'), Literal('o-antigen')))
    graph.add((gu('ge:0001065'), gu('rdfs:range'), gu(':spfyId')))

    # ge:0001077
    graph.add((gu('ge:0001077'), gu('rdf:type'), gu('owl:ObjectProperty')))
    graph.add((gu('ge:0001077'), gu('rdfs:comment'), Literal('h-antigen')))
    graph.add((gu('ge:0001077'), gu('rdfs:range'), gu(':spfyId')))

    # ge:0001684
    graph.add((gu('ge:0001684'), gu('rdf:type'), gu('owl:ObjectProperty')))
    graph.add((gu('ge:0001684'), gu('rdfs:comment'), Literal('k-antigen')))
    graph.add((gu('ge:0001684'), gu('rdfs:range'), gu(':spfyId')))

    # genome file class
    graph.add((gu('g:Genome'), gu('rdf:type'), gu('owl:Class')))
    graph.add((gu('g:Genome'), gu('rdfs:comment'), Literal('genome instance')))

    # Link genome file class and spfyid class.
    # If example=True, the reservation_triple() will do this instead.
    if not example:
        graph = link_uris(graph, gu(':spfyId'), gu('g:Genome'))

    # dc:date on g:Genome
    graph.add((gu('dc:date'), gu('rdf:type'), gu('owl:ObjectProperty')))
    graph.add((gu('dc:date'), gu('rdfs:comment'), Literal('submission date')))
    graph.add((gu('dc:date'), gu('rdfs:range'), gu('g:Genome')))

    # dc:description on g:Genome
    graph.add((gu('dc:description'), gu('rdf:type'), gu('owl:ObjectProperty')))
    graph.add((gu('dc:description'), gu('rdfs:comment'), Literal('class descriptor')))
    graph.add((gu('dc:description'), gu('rdfs:range'), gu('g:Genome')))

    # bag of contigs class
    graph.add((gu('so:0001462'), gu('rdf:type'), gu('owl:Class')))
    graph.add((gu('so:0001462'), gu('rdfs:comment'), Literal('bag of contigs')))

    # link bag of contigs
    graph = link_uris(graph, gu('g:Genome'), gu('so:0001462'))

    # contig class
    graph.add((gu('g:Contig'), gu('rdf:type'), gu('owl:Class')))
    graph.add((gu('g:Contig'), gu('rdfs:comment'), Literal('a contig')))

    # g:Identifier
    graph.add((gu('g:Identifier'), gu('rdf:type'), gu('owl:ObjectProperty')))
    graph.add((gu('g:Identifier'), gu('rdfs:comment'), Literal('accession number ie. record.id')))
    graph.add((gu('g:Identifier'), gu('rdfs:range'), gu('g:Contig')))

    # g:DNASequence
    graph.add((gu('g:DNASequence'), gu('rdf:type'), gu('owl:ObjectProperty')))
    graph.add((gu('g:DNASequence'), gu('rdfs:comment'), Literal('a dna sequence')))
    graph.add((gu('g:DNASequence'), gu('rdfs:range'), gu('g:Contig')))

    # g:Description
    graph.add((gu('g:Description'), gu('rdf:type'), gu('owl:ObjectProperty')))
    graph.add((gu('g:Description'), gu('rdfs:comment'), Literal('record.description')))
    graph.add((gu('g:Description'), gu('rdfs:range'), gu('g:Contig')))

    # faldo:Reference
    # here, we differ from faldo's implementation:
    # in faldo, it is diffined as an edge type
    # instead, we define it as an addition class type a g:Contig may have
    graph.add((gu('faldo:Reference'), gu('rdf:type'), gu('owl:Class')))
    graph.add((gu('faldo:Reference'), gu('rdf:comment'), Literal('a g:Contig that is referenced in some :Marker')))
    graph.add((gu('faldo:Reference'), gu('rdfs:subClassOf'), gu('g:Contig')))

    # faldo:Position
    graph.add((gu('faldo:Position'), gu('rdf:type'), gu('owl:Class')))
    graph.add((gu('faldo:ExactPosition'), gu('rdfs:subClassOf'), gu('faldo:Position')))
    graph.add((gu('faldo:ForwardStrandPosition'), gu('rdfs:subClassOf'), gu('faldo:ExactPosition')))
    graph.add((gu('faldo:ReverseStrandPosition'), gu('rdfs:subClassOf'), gu('faldo:ExactPosition')))

    # the faldo ontology defines the position number under faldo:position
    # note the lower-case
    graph.add((gu('faldo:position'), gu('rdf:type'), gu('owl:ObjectProperty')))
    graph.add((gu('faldo:position'), gu('rdfs:comment'), Literal('the numerical location of a position')))
    graph.add((gu('faldo:position'), gu('rdfs:range'), gu('faldo:Position')))

    # faldo:Begin faldo:End
    # here, we also differe from faldo's implementation
    # faldo implements it as an edge type to a blank node
    # we instead implement it as a class type applied to that blank node
    graph.add((gu('faldo:Begin'), gu('rdfs:subClassOf'), gu('faldo:Position')))
    graph.add((gu('faldo:End'), gu('rdfs:subClassOf'), gu('faldo:Position')))

    # link faldo:Position to faldo:Reference
    graph = link_uris(graph, gu('faldo:Reference'), gu('faldo:Position'))

    # faldo:Region
    graph.add((gu('faldo:Region'), gu('rdf:type'), gu('owl:Class')))
    graph.add((gu('faldo:Region'), gu('rdf:comment'), Literal('a region containing the start and the end positions')))

    # link faldo:Region with faldo:Begin and faldo:End
    graph = link_uris(graph, gu('faldo:Begin'), gu('faldo:Region'))
    graph = link_uris(graph, gu('faldo:End'), gu('faldo:Region'))

    # :Marker
    graph.add((gu(':Marker'), gu('rdf:type'), gu('owl:Class')))
    # the subclasses AntimicrobialResistanceGene and VirulenceFactor
    # were already defined in the generate_graph functions

    # link :Marker and faldo:Region
    graph = link_uris(graph, gu('faldo:Region'), gu(':Marker'))

    return write_graph(graph)

if __name__ == '__main__':
    print generate_ontology()
