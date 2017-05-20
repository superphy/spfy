import os
import pytest
import cPickle as pickle
from modules.beautify.beautify import beautify
from tests.constants import ARGS_DICT, BEAUTIFY_VF_SEROTYPE

def test_beautify():
    ## test vf & serotype json return
    vf_serotype_gene_dict = os.path.join('tests/refs', 'GCA_000005845.2_ASM584v2_genomic.fna_ectyper-vf_serotype.p')
    single_dict = dict(ARGS_DICT)
    single_dict.update({'i': vf_serotype_gene_dict})
    assert len(beautify(single_dict, vf_serotype_gene_dict)) == len(BEAUTIFY_VF_SEROTYPE)

    ## test serotype only json return
    # note: this is actually the same gene results file as above
    # we only differentiate what is returned to the user, because we want all analysis ran & added to the db
    # this mimicks user selection of serotype only
    single_dict.update({'options':{'vf': False, 'amr': False, 'serotype': True}})
    r = beautify(single_dict, vf_serotype_gene_dict)
    print r
    assert len(r) == 1
