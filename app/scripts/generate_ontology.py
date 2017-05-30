# baseURI: https://www.github.com/superphy#
from modules.turtleGrapher.turtle_grapher import generate_graph
from modules.turtleGrapher.turtle_utils import generate_uri as gu

def generate_ontology():
    '''
    Generates an ontology for the Spfy backend using utility methods used in
    production. Serializes the ontology as a turtle file, similar to faldo.ttl
    Recall that an ontology is really just a set of triples, but applied to
    classes/subclasses instead of specific instances.
    '''
    # generates the base graph with namespaces appended to it
    # also defines edge relations for :hasPart and :isFoundIn
    # also defines subclasses for our custom types
    graph = generate_graph()

    # adds info about this ontology being generated
    graph.add(())
