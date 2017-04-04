# usage:    cd app/
#           python -m pytest --ignore modules/ectyper/ecoli_serotyping

import pytest
import os
import cPickle as pickle

from modules.qc.qc import qc
from modules.blazeUploader.reserve_id import write_reserve_id
from modules.ectyper.call_ectyper import call_ectyper
from modules.amr.amr import amr
from modules.amr.amr_to_dict import amr_to_dict
from modules.beautify.beautify import beautify
from modules.turtleGrapher.datastruct_savvy import datastruct_savvy
from modules.turtleGrapher.turtle_grapher import turtle_grapher

# utility function to generate full path (still relative to root, not absoulte) for files in directories
def listdir_fullpath(d):
    valid_extensions = ('fasta','fna')
    l = []
    for f in os.listdir(d):
        filename, file_extension = os.path.splitext(f)
        if file_extension in valid_extensions:
            l.append(os.path.join(d, f))
    return l

# globals for testing
GENOMES_LIST_NOT_ECOLI = listdir_fullpath('tests/notEcoli')
GENOMES_LIST_ECOLI = listdir_fullpath('tests/ecoli')
ARGS_DICT={'disable_serotype':False,'disable_vf':False,'pi':90}

#### Non-Blazegraph/RQ Tests

def test_qc():
    for ecoli_genome in GENOMES_LIST_ECOLI:
        assert qc(ecoli_genome) == True
    for non_ecoli_genome in GENOMES_LIST_NOT_ECOLI:
        assert qc(non_ecoli_genome) == False

def test_ectyper():
    for ecoli_genome in GENOMES_LIST_ECOLI:
        single_dict = dict(ARGS_DICT)
        single_dict.update({'i':ecoli_genome})
        pickled_file = call_ectyper(single_dict)
        ectyper_dict = pickle.load(open(pickled_file,'rb'))
        assert type(ectyper_dict) == dict

def test_amr():
    for ecoli_genome in GENOMES_LIST_ECOLI:
        pickled_file = amr(ecoli_genome)
        ectyper_dict = pickle.load(open(pickled_file,'rb'))
        assert type(ectyper_dict) == dict
