import os
import pytest
import cPickle as pickle
from modules.beautify.beautify import beautify
from tests.constants import ARGS_DICT, BEAUTIFY_VF_SEROTYPE

def test_beautify():
    vf_serotype_gene_dict = os.path.join('tests/refs', 'GCA_000005845.2_ASM584v2_genomic.fna_ectyper-vf_serotype.p')
    gene_dict = pickle.load(open(vf_serotype_gene_dict, 'rb'))
    single_dict = ARGS_DICT + {'i': vf_serotype_gene_dict}
    assert beautify(single_dict, gene_dict) == BEAUTIFY_VF_SEROTYPE
