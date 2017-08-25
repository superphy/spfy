import cPickle as pickle
from rdflib import BNode, Literal, Graph
from modules.turtleGrapher.turtle_utils import generate_uri as gu, generate_hash, link_uris
from modules.turtleGrapher.turtle_grapher import generate_graph
from modules.blazeUploader.upload_graph import upload_graph
from modules.PanPredic.pan_utils import contig_name_parse
# working with Serotype, Antimicrobial Resistance, & Virulence Factor data
# structures

def parse_serotype(graph, serotyper_dict, uriIsolate):
    if 'O type' in serotyper_dict:
        graph.add((uriIsolate, gu('ge:0001076'),
                   Literal(serotyper_dict['O type'])))
    if 'H type' in serotyper_dict:
        graph.add((uriIsolate, gu('ge:0001077'),
                   Literal(serotyper_dict['H type'])))
    if 'K type' in serotyper_dict:
        graph.add((uriIsolate, gu('ge:0001684'),
                   Literal(serotyper_dict['K type'])))

    return graph


def parse_gene_dict(graph, gene_dict, uriGenome, geneType):
    '''
    My intention is to eventually use ECTyper for all of the calls it was meant for.
    Just need to update ECTyper dict format to ref. AMR / VF by contig. as opposed to genome directly.

    These are the common gene related triples to both AMR / VF.
    Note: we are working from uriGenome and assume that the calling functions (
    generate_amr() and generate_vf() are doing the transformations to the
    gene_dict.keys so that they are contig ids (as they differ in return value
    between VF & AMR from ECTyper)
    )

    TODO: offshore rgi calls to ectyper and make it return a dict in the format we need
    -currently, we'll handle ORF_ID to contig id transform in generate_amr()

    Args:
        graph(rdflib.Graph): the running graph with all our triples
        gene_dict({{}}): a dictionary of genes with a assoc info
            ex. {'Some_Contig_ID':[{'START','STOP','ORIENTATION','GENE_NAME'}]}
        uriGenome(rdflib.URIRef): the base uri of the genome
            ex. :4eb02f5676bc808f86c0f014bbce15775adf06ba


    TODO: merge common components with generate_amr()
    '''

    for contig_id in gene_dict:
        #makes sure that the contigs are named correctly
        #contig_name = contig_name_parse(contig_id)
        '''
        if contig_name != contig_id:
            gene_dict[contig_name] = gene_dict[contig_id]
            del gene_dict[contig_id]
        '''
        for gene_record in gene_dict[contig_id]:
            # uri for bag of contigs
            # ex. :4eb02f5676bc808f86c0f014bbce15775adf06ba/contigs/
            #make sure that uriGenome is a genome and not a string
            uriGenomes = gu(uriGenome)
            uriContigs = gu(uriGenomes, "/contigs")
            # recreating the contig uri
            
            uriContig = gu(uriContigs, '/' + contig_id)
            
          

            # after this point we switch perspective to the gene and build down to
            # relink the gene with the contig
            bnode_region = BNode()
            bnode_start = BNode()
            bnode_end = BNode()

            # some gene names, esp those which are effectively a description,
            # have spaces
            gene_name = gene_record['GENE_NAME'].replace(' ', '_')
            uriGene = gu(':' + gene_name)
            # define the object type of the gene
            graph.add((uriGene, gu('rdf:type'), gu(':' + geneType)))
            # human-readable
            graph.add((uriGene, gu('dc:description'), Literal(gene_name)))

            # define the object type of bnode_region
            graph.add((bnode_region, gu('rdf:type'), gu('faldo:Region')))
            # link the region (eg. the occurance of the gene in a contig)
            graph = link_uris(graph, bnode_region, uriGene)
            #graph.add((uriGene, gu(':hasPart'), bnode_region))

            # define the object type of the start & end bnodes
            graph.add((bnode_start, gu('rdf:type'), gu('faldo:Begin')))
            graph.add((bnode_end, gu('rdf:type'), gu('faldo:End')))
            # link the start and end bnodes to the region
            graph = link_uris(graph, bnode_start, bnode_region)
            graph = link_uris(graph, bnode_end, bnode_region)
            #graph.add((bnode_region, gu(':hasPart'), bnode_start))
            #graph.add((bnode_region, gu(':hasPart'), bnode_end))

            # this is a special case for amr results
            if 'CUT_OFF' in gene_dict:
                graph.add((bnode_start, gu('dc:Description'),
                           Literal(gene_dict['CUT_OFF'])))
                graph.add((bnode_end, gu('dc:Description'),
                           Literal(gene_dict['CUT_OFF'])))

            # object types defined in FALDO standard
            graph.add((bnode_start, gu('rdf:type'), gu('faldo:Position')))
            graph.add((bnode_start, gu('rdf:type'), gu('faldo:ExactPosition')))
            graph.add((bnode_end, gu('rdf:type'), gu('faldo:Position')))
            graph.add((bnode_end, gu('rdf:type'), gu('faldo:ExactPosition')))

            if 'ORIENTATION' in gene_record:
                if gene_record['ORIENTATION'] is '+':
                    graph.add((bnode_start, gu('rdf:type'), gu(
                        'faldo:ForwardStrandPosition')))
                    graph.add((bnode_end, gu('rdf:type'), gu(
                        'faldo:ForwardStrandPosition')))
                else:
                    graph.add((bnode_start, gu('rdf:type'), gu(
                        'faldo:ReverseStrandPosition')))
                    graph.add((bnode_end, gu('rdf:type'), gu(
                        'faldo:ReverseStrandPosition')))

            if geneType == 'PanGenomeRegion':
                graph = link_uris(graph, uriGenomes, uriGene)
                graph.add((uriGene, gu('g:DNASequence'),
                           Literal(gene_record['DNASequence'])))

            graph.add((bnode_start, gu('faldo:Position'),
                       Literal(gene_record['START'])))
            graph.add((bnode_end, gu('faldo:Position'),
                       Literal(gene_record['STOP'])))
            # because we've identified a gene, that uriContig is now also a faldo:Reference (note: this isn't how FALDO intended the linkage to be, but we do this to accomadate inferencing in Blazegraph)
            # this also means that if you find (or are querying) a uriContig and it isn't not a faldo:Reference (& only a g:Contig) then there are no genes assoc w it
            graph.add((uriContig, gu('rdf:type'), gu('faldo:Reference')))
            # link up the start/end bnodes to the contig
            graph = link_uris(graph, uriContig, bnode_start)
            graph = link_uris(graph, uriContig, bnode_end)
            #graph.add((bnode_start, gu(':hasPart'), uriContig))
            #graph.add((bnode_end, gu(':hasPart'), uriContig))

    #### end of nested for

    return graph

def generate_datastruct(query_file, id_file, pickled_dictionary):
    '''
    This is simply to decouple the graph generation code from the
    upload code. In RQ backend, the datastruct_savvy() method is called
    where-as in savvy.py (without RQ or Blazegraph) only compute_datastruct()
    is called. The return type must be the same in datastruct_savvy to
    maintain backwards compatability, hence most of the code is stored here
    instead.
    '''
    # Base graph generation
    graph = generate_graph()

    # uriGenome generation
    file_hash = generate_hash(query_file)
    uriGenome = gu(':' + file_hash)

    # uriIsolate retrieval
    with open(id_file) as f:
        l = f.readline()
        spfyid = int(l)
    uriIsolate = gu(':spfy' + str(spfyid))

    # results dict retrieval
    results_dict = pickle.load(open(pickled_dictionary, 'rb'))

    # graphing functions
    for key in results_dict.keys():
        if key == 'Serotype':
            graph = parse_serotype(graph,results_dict['Serotype'],uriIsolate)
        elif key == 'Virulence Factors':
            graph = parse_gene_dict(graph, results_dict['Virulence Factors'], uriGenome, 'VirulenceFactor')
        elif key == 'Antimicrobial Resistance':
            graph = parse_gene_dict(graph, results_dict['Antimicrobial Resistance'], uriGenome,
                                    'AntimicrobialResistanceGene')
        #elif key == 'PanGenomeRegion':
         #   graph = parse_gene_dict(graph, results_dict[key], uriGenome, key)

    return graph

def datastruct_savvy(query_file, id_file, pickled_dictionary):
    """
    Note: we work we base graphs (those generated solely from the fasta file) and result graphs (those generated from analysis modules (RGI/ECtyper) separately - they are only linked once uploaded to blazegraph
    :param args_dict:
    :return:
    """
    graph = generate_datastruct(query_file, id_file, pickled_dictionary)
    return upload_graph(graph)
