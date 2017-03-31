# a collection of turtle generation functions
# not meant to be run directly
# only contains functions related to rdflib.Graph manipulation
# only nonspecific stuff: shouldn't contain any functions directly related
# to data structure(rdf triple organization) of the modules you're dev'ing

from app import config
from modules.turtleGrapher.turtle_utils import generate_hash, generate_uri as gu
from modules.blazeUploader.upload_graph import upload_graph
from rdflib import Namespace, Graph, Literal, plugin
from Bio import SeqIO
from os.path import basename

def generate_graph():
    '''
    Parses all the Namespaces defined in the config file and returns a graph
    with them bound.

    Return:
        (rdflib.Graph): a graph with all the defined Namespaces bound to it.
    '''

    graph = Graph()

    for key in config.namespaces.keys():
        if key is 'root':
            graph.bind('', config.namespaces['root'])
        else:
            graph.bind(key, config.namespaces[key])

    return graph

def generate_turtle_skeleton(query_file):
    '''
    Handles the main generation of a turtle object.

    NAMING CONVENTIONS:
    uriIsolate: this is the top-most entry, a uniq. id per file is allocated by checking our DB for the greatest most entry (not in this file)
        ex. :spfy234
    uriAssembly: aka. the genome ID, this is a sha1 hash of the file contents
        ex. :4eb02f5676bc808f86c0f014bbce15775adf06ba
    uriContig: indiv contig ids; from SeqIO.record.id - this should be uniq to a contig (at least within a given file)
        ex. :4eb02f5676bc808f86c0f014bbce15775adf06ba/contigs/FLOF01006689.1
        note: the record.id is what RGI uses as a prefix for ORF_ID (ORF_ID has additional _314 or w/e #s)

    Args:
       query_file(str): path to the .fasta file (this should already incl the directory)
    Returns:
        graph: the graph with all the triples generated from the .fasta file
    '''
    # Base graph generation
    graph = generate_graph()

    # uriGenome generation
    file_hash = generate_hash(query_file)
    uriGenome = gu(':' + file_hash)

    # this is used as the human readable display of Genome
    graph.add((uriGenome, gu('dc:description'), Literal(basename(query_file))))
    # note that timestamps are not added in base graph generation, they are only added during the check for duplicate files in blazegraph

    # uri for bag of contigs
    # ex. :4eb02f5676bc808f86c0f014bbce15775adf06ba/contigs/
    uriContigs = gu(uriGenome, "/contigs")
    graph.add((uriGenome, gu('so:0001462'), uriContigs))

    for record in SeqIO.parse(open(query_file), "fasta"):
        # ex. :4eb02f5676bc808f86c0f014bbce15775adf06ba/contigs/FLOF01006689.1
        uriContig = gu(':' + record.id)
        # linking the spec contig and the bag of contigs
        graph.add((uriContigs, gu('g:Contig'), uriContig))
        graph.add((uriContig, gu('g:DNASequence'), Literal(record.seq)))
        graph.add((uriContig, gu('g:Description'),
                   Literal(record.description)))
        graph.add((uriContig, gu('dc:description'),
                   Literal(record.description)))

    return graph

def turtle_grapher(query_file):
    graph = generate_turtle_skeleton(query_file)
    return upload_graph(graph)
