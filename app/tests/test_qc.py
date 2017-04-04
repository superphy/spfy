# usage:    cd app/
#           python -m pytest

import pytest
import os

from modules.qc.qc import qc
from modules.blazeUploader.reserve_id import write_reserve_id
from modules.ectyper.call_ectyper import call_ectyper
from modules.amr.amr import amr
from modules.amr.amr_to_dict import amr_to_dict
from modules.beautify.beautify import beautify
from modules.turtleGrapher.datastruct_savvy import datastruct_savvy
from modules.turtleGrapher.turtle_grapher import turtle_grapher

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

GENOMES_LIST_NOT_ECOLI = listdir_fullpath('tests/notEcoli')
GENOMES_LIST_ECOLI = listdir_fullpath('tests/ecoli')

def test_qc():
    for ecoli_genome in GENOMES_LIST_ECOLI:

        print ecoli_genome
        assert qc(non_ecoli_genome) == True
    for non_ecoli_genome in GENOMES_LIST_NOT_ECOLI:
        print non_ecoli_genome
        assert qc(non_ecoli_genome) == False
