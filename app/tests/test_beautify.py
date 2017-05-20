import os
import pytest
import cPickle as pickle
from modules.beautify.beautify import beautify, json_return
from tests.constants import ARGS_DICT, BEAUTIFY_VF_SEROTYPE

vf_serotype_gene_dict = os.path.join('tests/refs', 'GCA_000005845.2_ASM584v2_genomic.fna_ectyper-vf_serotype.p')

def test_beautify_vf_serotype():
    ## test vf & serotype json return
    single_dict = dict(ARGS_DICT)
    single_dict.update({'i': vf_serotype_gene_dict})
    assert len(beautify(single_dict, vf_serotype_gene_dict)) == len(BEAUTIFY_VF_SEROTYPE)

def test_beautify_serotype_only():
    ## test serotype only json return
    # note: this is actually the same gene results file as above
    # we only differentiate what is returned to the user, because we want all analysis ran & added to the db
    single_dict = dict(ARGS_DICT)
    single_dict.update({'i': vf_serotype_gene_dict})
    # this mimicks user selection of serotype only
    single_dict.update({'options':{'vf': False, 'amr': False, 'serotype': True}})
    # beautify is what is actually called by the RQ worker & returned to the user
    r = beautify(single_dict, vf_serotype_gene_dict)
    print r
    assert len(r) == 1

def test_beautify_json_r_serotype_only()
    single_dict = dict(ARGS_DICT)
    single_dict.update({'i': vf_serotype_gene_dict})
    # this mimicks user selection of serotype only
    single_dict.update({'options':{'vf': False, 'amr': False, 'serotype': True}})
    ## test json_r separately of failed handling
    # json_return() is a part of the beautify work
    gene_dict = pickle.load(open(vf_serotype_gene_dict, 'rb'))
    r = json_return(single_dict, gene_dict)
    assert len(r) == 1
