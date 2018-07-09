# usage:    cd app/
#           python -m pytest --ignore modules/ectyper/ecoli_serotyping -v

import pytest
import os
import subprocess
import cPickle as pickle
import pandas as pd

from modules.qc.qc import qc, check_header_parsing, check_ecoli
from middleware.blazegraph.reserve_id import reserve_id
from modules.ectyper.call_ectyper import call_ectyper_vf, call_ectyper_serotype
from modules.amr.amr import amr
from modules.amr.amr_to_dict import amr_to_dict
from middleware.display.beautify import beautify
from middleware.graphers.datastruct_savvy import datastruct_savvy
from middleware.graphers.turtle_grapher import turtle_grapher
from middleware.models import unpickle

from tests.utils import listdir_fullpath
from tests.constants import ARGS_DICT, AMR_HEADERS

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

def test_ectyper_vf(return_one=False):
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
        if return_one:
            return json_return

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
        assert isinstance(serotype_model, list)

def test_ectyper_serotype_call_pickle(return_one=False):
    """
    Check the actual call from Spfy's code.
    """
    for ecoli_genome in GENOMES_LIST_ECOLI:
        single_dict = dict(ARGS_DICT)
        single_dict.update({'i':ecoli_genome})
        # Pickle the model, and return the path to the file.
        pickled_serotype_model = call_ectyper_serotype(single_dict)
        ectyper_serotype_model = unpickle(pickled_serotype_model)
        assert isinstance(ectyper_serotype_model, list)
        if return_one:
            return ectyper_serotype_model

def test_amr():
        ecoli_genome = GENOMES_LIST_ECOLI[0]
        # this generates the .tsv
        pickled_amr_tsv = amr(ecoli_genome)
        filename, file_extension = os.path.splitext(pickled_amr_tsv)
        assert file_extension == '.tsv'

        # Indices check.
        df = pd.read_table(pickled_amr_tsv)
        headers = df.columns.values
        assert set(AMR_HEADERS).issubset(set(headers))

        # convert the tsv to a directory
        pickled_amr_dict = amr_to_dict(pickled_amr_tsv)
        amr_dict = pickle.load(open(pickled_amr_dict,'rb'))
        assert type(amr_dict) == dict

        # beautify amr check
        single_dict = dict(ARGS_DICT)
        single_dict.update({'i':ecoli_genome})
        json_return = beautify(pickled_amr_dict, single_dict)
        assert type(json_return) == list
