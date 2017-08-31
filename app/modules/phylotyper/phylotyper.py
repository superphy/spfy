"""Phylotyper module

Start phylotyper job. Uses default result directories

Example:
    :

        $ python example_google.py

"""

import subprocess
import os
import shutil
import logging
from tempfile import mkdtemp
import pandas as pd
import cPickle as pickle

import config
from modules.turtleGrapher import turtle_utils
from modules.phylotyper import ontology, exceptions
from modules.phylotyper.sequences import MarkerSequences

logger = logging.getLogger(__name__)



def phylotyper(query, subtype, result_file):
    '''
    Wrapper for Phylotyper

    Args:
        query (str): Genome URI
        subtype (str): Phylotyper recognized subtype (e.g. stx1)
        result_file (str): File location to write phylotyper tab-delim result to

    Returns:
        file to tab-delimited text results
    
    '''

    # Validate subtype ontology
    try:
        ontology.load(subtype)
    except exceptions.DatabaseError as err:
        logger.error('Please run VF detection before calling Phylotyper. Error message: {}'.format(err))
    except Exception as err:
        logger.error('Unexpected error from phylotyper ontology loading. Error message: {}'.format(err))
        raise err


    # Get loci to use in subtype prediction
    uri = 'subt:'+subtype
    loci_results = ontology.schema_query(uri)
    loci = [ turtle_utils.generate_uri(l['locus']) for l in sorted(loci_results, key=lambda k: k['i'])]

    # Get alleles for this genome
    markerseqs = MarkerSequences(loci)
    fasta = markerseqs.fasta(query)

    temp_dir = mkdtemp(prefix='pt', dir=config.DATASTORE)
    query_file = os.path.join(temp_dir, 'query.fasta')
    output_file = os.path.join(temp_dir, 'subtype_predictions.tsv')

    if fasta:
        # Run phylotyper
        with open(query_file, 'w') as fh:
            fh.write(fasta)

        subprocess.call(['phylotyper', 'genome', '--noplots',
                         subtype,
                         temp_dir,
                         query_file])

    else:
        # No loci
        # Report no loci status in output
        with open(output_file, 'w') as fh:
            fh.write("#Empty Header")
            fh.write("Required alleles not found")

    shutil.move(output_file, result_file)
    shutil.rmtree(temp_dir)
          
    return result_file


def to_dict(pt_file, subtype, pickle_file):
    """ Convert output into intermediate output

      Returns pickled dictionary indexed by subtype predictions

    """
      
    pt_results = pd.read_table(pt_file)
    
    pt_results = pt_results[['subtype','probability','loci']]

    pt_results = pt_results.to_dict()
    pt_results['contig'] = {}
    pt_results['start'] = {}
    pt_results['stop'] = {}

    # Parse marker URIs, starts, stops, etc from loci field
    # Discard rest
    for k, v in pt_results['loci'].iteritems():
        loci = eval(v)
        contigs = []
        starts = []
        stops = []
        locis = []
        for l in loci:
            datasections = l.split(" ")
            locsections = datasections[2].split(":")
            contigs.append(locsections[-3])
            starts.append(int(locsections[-2].split('..')[0]) - int(locsections[-1].split('-')[0]) - 1)
            stops.append(int(locsections[-2].split('..')[1]) - int(locsections[-1].split('-')[1]) - 1)
            locis.append(datasections[1])

        pt_results['loci'][k] = locis
        pt_results['contig'][k] = contigs
        pt_results['start'][k] = starts
        pt_results['stop'][k] = stops
    
    pickle.dump(pt_results, open(pickle_file, 'wb'))

    return pickle_file


def beautify(p_file):
    """ Convert phylotyper data into json format used by front end


    """

    pt_dict = pickle.load(open(p_file, 'rb'))

    print(pt_dict)

    # Expand into table rows - one per loci
    table_rows = []
    for k in pt_dict['loci']:
        
        # Location info
        for i in range(len(pt_dict['loci'][k])):
            instance_dict = {}
            instance_dict['start'] = pt_dict[k]['start'][i]
            instance_dict['stop'] = pt_dict[k]['stop'][i]
            instance_dict['contig'] = pt_dict[k]['contig'][i]
            

            # Genome
            # Subtype info
            instance_dict['subtype'] = pt_dict[k]['subtype']
            instance_dict['probability'] = pt_dict[k]['probability']
        

            table_rows.append(instance_dict)
            

    return table_rows
        



def savvy(p_file, subtype):
    """ Load phylotyper results into DB



    """

    uri = 'subt:'+subtype

    # Get list of permissable subtype values
    subtypes_results = ontology.subtypeset_query(uri)
    subtypes = {}
    for r in subtypes_results:
        subtypes[ r['value'] ] = turtle_utils.generate_uri(r['part'])

    pt_dict = pickle.load(open(p_file, 'rb'))
    

def ignorant(p_file, subtype):
    pass




if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-g",
        help="Genome URI",
        required=True
    )
    parser.add_argument(
        "-s",
        help="Phylotyper subtype scheme",
        required=True
    )
    args = parser.parse_args()

    input_g = args.g
    if input_g.startswith('<'):
        input_g = input_g[1:-1]
    g = turtle_utils.fulluri_to_basename(turtle_utils.generate_uri(input_g))
    pt_file = os.path.join(config.DATASTORE, g+'_pt.tsv')
    pickle_file = os.path.join(config.DATASTORE, g+'_pt.p')
    
    # phylotyper(args.g, args.s, pt_file)
    #to_dict(pt_file, args.s, pickle_file)
    beautify(pickle_file)
    #savvy(pickle_file, args.s)