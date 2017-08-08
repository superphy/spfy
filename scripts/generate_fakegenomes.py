import os
from random import randint
from Bio import SeqIO

def create_fake(f, fake_dir):
    # generate a seed to prepend to contig ids
    # this is required as spfy implements hash checking to avoid duplicates
    seed = randint(1000000,9999999)
    seed = 'test' + str(seed) + '_'

    # create a filename for this fake
    fake_name = os.path.basename(f)
    fake_name = seed + fake_name

    # open a new file for the fake
    with open(os.path.join(fake_dir,fake_name), 'w') as fl:
        # step through the contigs
        for record in SeqIO.parse(open(f), "fasta"):
            # write the new header
            fl.write('>' + seed + record.description + '\n')
            # write the old sequence
            fl.write(record.sequence + '\n')

def gen(directory, n):
    # create a directory for the fakes
    fake_dir = os.path.join(directory,'fakes')
    if not os.path.exists(fake_dir):
        os.makedirs(fake_dir)

    seeds = []
    # walk the directory and grab all the files
    for root, dirs, files in os.walk(os.path.abspath(directory)):
        for file in files:
            seeds.append(os.path.join(root, file))

    # start a count for the number of files generated
    c = 0
    # check how many seed files were supplied
    len_seeds = len(seeds)
    # begin generating files
    while c < n:
        # create a pointer for where you are in the list of seed files
        p = 0
        while p < len_seeds-1:
            create_fake(seeds[p], fake_dir)
            p += 1

if __name__ == "__main__":
    import argparse

    # parsing cli-input
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        help="Directory of .fasta files",
        required=True
    )
    parser.add_argument(
        "-n",
        help="The number of fake genomes you want",
        required=True
    )
    args = parser.parse_args()

    gen(args.i, args.n)
