import subprocess
import pandas as pd

from app.modules.turtleGrapher import datastruct_savvy

def generate_amr(graph, uriGenome, fasta_file):


    if '/' in fasta_file:
        outputname = fasta_file.split('/')[-1]
    else:
        outputname = fasta_file

    # differs from ectyper as we dont care about the temp results, just the final .tsv
    # direct (the main) call
    print subprocess.call(['rgi',
                     '-i', fasta_file,
                     '-o', outputname])

    print fasta_file


    # the rgi_json call in rgitool.py isn't needed for us
    # this generates the .tsv we want
    subprocess.call(['rgi_jsontab',
                     '-i', outputname + '.json',
                     '-o', outputname])



    #rename(output + '.txt', output + '.tsv')

    amr_results = pd.read_table('/app/' + outputname + '.txt')
    amr_results = amr_results[
        ['ORF_ID', 'START', 'STOP', 'ORIENTATION', 'CUT_OFF', 'Best_Hit_ARO']]

    amr_results.rename(
        columns={'ORF_ID': 'contig_id', 'Best_Hit_ARO': 'GENE_NAME'}, inplace=True)

    # sometimes there are spaces at the end of the contig id, also we remove
    # the additional occurance tag that RGI adds to contig ids
    amr_results['contig_id'] = amr_results['contig_id'].apply(
        lambda n: n.strip().rsplit('_', 1)[0])

    # note: you might be tempted to prefix a set_index('contig_id') but
    # remember, the same contig might have multiple genes
    amr_results = amr_results.to_dict(orient='index')

    # we have to manually check for contigs with multiple genes
    # TODO: write something less horrendously slow and memory consuming
    amr_dict = {}
    for i in amr_results.keys():
        contig_id = amr_results[i]['contig_id']
        if contig_id not in amr_dict.keys():
            amr_dict[contig_id] = []
        amr_dict[contig_id].append(dict((keys, amr_results[i][keys]) for keys in (
            'START', 'STOP', 'GENE_NAME', 'ORIENTATION', 'CUT_OFF', 'GENE_NAME')))
    # wipe the amr_results early
    amr_results = None

    graph = datastruct_savvy.parse_gene_dict(graph, amr_dict, uriGenome)

    return {'graph': graph, 'amr_dict': amr_dict}

def amr():
    '''
    (1) Creates a blank graph object
    (2) Generates the URIs required for appending AMR data to the graph object.
    (3) Uses RGI to compute AMR results
    (4)
        a. If called with deployment flag, sends AMR to beautify.py for processing to be returned in spfy web app.
        b. If a blazegraph url was supplied, cals datastruct.
    :return:
    '''
    from app.modules.turtleGrapher.turtle_grapher import generate_graph
    graph = generate_graph()