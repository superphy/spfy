# baseURI: https://www.github.com/superphy#
from rdflib import Literal
from modules.turtleGrapher.turtle_grapher import generate_graph
from modules.turtleGrapher.turtle_utils import generate_uri as gu, link_uris

def generate_ontology():
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

    # link genome file class and spfyid class
    graph = link_uris(graph, gu(':spfyId'), gu('g:Genome'))

    return write_graph(graph)

if __name__ == '__main__':
    print generate_ontology()
