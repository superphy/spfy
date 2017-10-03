# loads all the reference Virulence Factors
import os
import shutil
import requests
from tempfile import TemporaryFile
from shutil i
from modules.turtleGrapher.turtle_grapher import generate_graph

def get_ref_vfs():
    tf = TemporaryFile()
    # try to get the VF ref file from github
    try:
        f = requests.get('https://raw.githubusercontent.com/phac-nml/ecoli_vf/master/data/repaired_ecoli_vfs_shortnames.ffn')
        print 'Retrieved ref vf file from GitHub.'
        # github return Unicdoe, we want the str
        tf.write(str(f.text))
    except:
        # if fails, use the backup copy in superphy/backend 's ECTyper submodule
        print 'Could not retrieve ecoli_vf from GitHub. Using backup...'
        f = 'modules/ectyper/ecoli_serotyping/Data/repaired_ecoli_vfs_shortnames.ffn'
        with open(f,'r+b') as fl:
            shutil.copyfileobj(fl,tf)
    return tf

def identify_name(line):
    '''
    Determines the name of the gene in a given header.
    '''
    sub = ''
    if ')' in  line:
        if 'gi:' in line:
            sub = line.split('(')[2].split(')')[0]
        else:
            sub = line[line.find("(")+1:line.find(")")]
    return sub

def load_refs():
    # get the reference VF file as a tempfile.TemporaryFile
    f = get_ref_vfs()

    # read this reference file write in into a list
    lines = []
    with open(fname) as f:
        lines = [line.rstrip('\n') for line in f]

    # create a blank graph object
    g = generate_graph()

    # iterate using i for the header's position
    for i in range(0,len(lines),2):
        sub = identify_name(lines[i])
