import os
import pytest
import cPickle as pickle
from modules.beautify.beautify import beautify
from tests.constants import ARGS_DICT, BEAUTIFY_VF_SEROTYPE

def test_beautify():
    vf_serotype_gene_dict = os.path.join('tests/refs', 'GCA_000005845.2_ASM584v2_genomic.fna_ectyper-vf_serotype.p')
    single_dict = dict(ARGS_DICT)
    single_dict.update({'i': vf_serotype_gene_dict})
    assert beautify(single_dict, vf_serotype_gene_dict) == BEAUTIFY_VF_SEROTYPE
