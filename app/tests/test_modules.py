# usage:    cd app/
#           python -m pytest --ignore modules/ectyper/ecoli_serotyping -v

import pytest
import os
import subprocess
import cPickle as pickle
import pandas as pd

from modules.qc.qc import qc, check_header_parsing, check_ecoli
from middleware.blazegraph.reserve_id import write_reserve_id
from modules.ectyper.call_ectyper import call_ectyper_vf, call_ectyper_serotype
from modules.amr.amr import amr
from modules.amr.amr_to_dict import amr_to_dict
from middleware.display.beautify import beautify, model_to_json
from middleware.graphers.datastruct_savvy import datastruct_savvy
from middleware.graphers.turtle_grapher import turtle_grapher
from middleware.models import unpickle

from tests.constants import ARGS_DICT

# utility function to generate full path (still relative to root, not absoulte) for files in directories
def listdir_fullpath(d):
    valid_extensions = ('.fasta','.fna')
    l = []
    for f in os.listdir(d):
        filename, file_extension = os.path.splitext(f)
        if file_extension in valid_extensions:
            l.append(os.path.join(d, f))
    return l

# globals for testing
GENOMES_LIST_NOT_ECOLI = listdir_fullpath('tests/notEcoli')
GENOMES_LIST_ECOLI = listdir_fullpath('tests/ecoli')
GENOMES_LIST_HEADERS = listdir_fullpath('tests/headers')

#### Non-Blazegraph/RQ Tests

# QC-related test.
def test_ecoli_checking():
    for ecoli_genome in GENOMES_LIST_ECOLI:
        assert check_ecoli(ecoli_genome) == True
    for non_ecoli_genome in GENOMES_LIST_NOT_ECOLI:
        assert check_ecoli(non_ecoli_genome) == False

# QC-related test.
def test_header_parsing():
    # Test header parsing for general E.Coli genomes.
    for ecoli_genome in GENOMES_LIST_ECOLI:
        assert check_header_parsing(ecoli_genome) == True

    # Test header parsing for genomes we're having problems with.
    for ecoli_genome in GENOMES_LIST_HEADERS:
        assert check_header_parsing(ecoli_genome) == True

# QC-related test.
def test_qc():
    for ecoli_genome in GENOMES_LIST_ECOLI:
        assert qc(ecoli_genome) == True
    for non_ecoli_genome in GENOMES_LIST_NOT_ECOLI:
        assert qc(non_ecoli_genome) == False

def test_ectyper_vf():
    """Check the ECTyper from `superphy` which is used for virulance factor
    identification. Installed as a submodule in the `modules` directory.
    """
    for ecoli_genome in GENOMES_LIST_ECOLI:
        # basic ECTyper check
        single_dict = dict(ARGS_DICT)
        single_dict.update({'i':ecoli_genome})
        pickled_ectyper_dict = call_ectyper_vf(single_dict)
        ectyper_dict = pickle.load(open(pickled_ectyper_dict,'rb'))
        assert type(ectyper_dict) == dict

        # beautify ECTyper check
        json_return = beautify(pickled_ectyper_dict, single_dict)
        assert type(json_return) == list

def _validate_model(model):
    # Validate (throws error if invalidate).
    model.validate()
    # Check that the return rows is not some random empty list.
    assert model.rows
    # Check the conversion for the front-end.
    r = model_to_json(model)
    # This is not really json; more like a list than a dict structure.
    assert isinstance(r, list)
    # Check that this isn't empty.
    assert r

def test_ectyper_serotype_direct():
    """Check the ECTyper from `master` which only performs serotyping.
    Installed in the conda environment.
    """
    for ecoli_genome in GENOMES_LIST_ECOLI:
        # Check that the conda env can run ectyper.
        ret_code = subprocess.call(['ectyper', '-i', ecoli_genome])
        assert ret_code == 0

def test_ectyper_serotype_call_nopickle():
    """
    Check the actual call from Spfy's code.
    """
    for ecoli_genome in GENOMES_LIST_ECOLI:
        single_dict = dict(ARGS_DICT)
        single_dict.update({'i':ecoli_genome})
        # Have the call return the model without pickling.
        serotype_model = call_ectyper_serotype(single_dict, pickle=False)
        _validate_model(serotype_model)

def test_ectyper_serotype_call_pickle():
    """
    Check the actual call from Spfy's code.
    """
    for ecoli_genome in GENOMES_LIST_ECOLI:
        single_dict = dict(ARGS_DICT)
        single_dict.update({'i':ecoli_genome})
        # Pickle the model, and return the path to the file.
        pickled_serotype_model = call_ectyper_serotype(single_dict)
        ectyper_serotype_model = unpickle(pickled_serotype_model)
        _validate_model(pickled_serotype_model)

def test_amr():
        ecoli_genome = GENOMES_LIST_ECOLI[0]
        # this generates the .tsv
        pickled_amr_tsv = amr(ecoli_genome)
        filename, file_extension = os.path.splitext(pickled_amr_tsv)
        assert file_extension == '.tsv'

        # convert the tsv to a directory
        pickled_amr_dict = amr_to_dict(pickled_amr_tsv)
        amr_dict = pickle.load(open(pickled_amr_dict,'rb'))
        assert type(amr_dict) == dict

        # beautify amr check
        single_dict = dict(ARGS_DICT)
        single_dict.update({'i':ecoli_genome})
        json_return = beautify(pickled_amr_dict, single_dict)
        assert type(json_return) == list
