# to be run from within a Docker container
# allows bypassing of reactapp front-end to load genome files into RQ
import os
from modules.spfy import spfy

def create_request(f):
    '''
    Args:
        f (str): genome file with absolute path
            ex. '/datastore/GCA_001911305.1_ASM191130v1_genomic.fna'
    '''
    # create a blank dictionary which is used as input for spfy
    d = {}
    # add defaults for options
    pi = 90
    d['pi'] = pi
    options = {
        'amr': True,
        'vf': True,
        'serotype': True,
        'bulk': True,
        'pi': pi
    }
    d['options'] = options
    # add the file
    d['i'] = f
    return d

def load(directory='/datastore'):
    list_files = []
    # walk the directory and grab all the files
    for root, dirs, files in os.walk(os.path.abspath(directory)):
        for file in files:
            list_files.append(os.path.join(root, file))
    len_files = len(list_files)
    p = 0
    while p < len_files-1:
        d = create_request(list_files[p])
        spfy(d)
        print str(p+1) + '/' + str(len_files) + ' enqueued'
        p += 1

if __name__ == "__main__":
    import argparse

    # parsing cli-input
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        help="Directory of .fasta files",
        required=False,
        default='/datastore'
    )
    args = parser.parse_args()

    load(args.i)
