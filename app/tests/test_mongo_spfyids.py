import mock
import config

from middleware.graphers.turtle_utils import generate_hash, generate_uri as gu
from tests.utils import listdir_fullpath

from middleware.blazegraph.reserve_id import _check

GENOMES_LIST_ECOLI = listdir_fullpath('tests/ecoli')

class MockMongo():

    def __init__(self):
        self.d = {
            'spfyid': 0
        }

    def mongo_find(self, uid, key='store', collection=''):
        return self.d[uid]

    def mongo_update(self, uid, json, key='store', collection=''):
        self.d.update({uid: json})


class TestDuplicateDefaults(object):

    m = MockMongo()

    @mock.patch('mongo_find', side_effect=m.mongo_find)
    def test_duplicate_defaults(self):
        '''Should start spfyids at 0 and inrement by 1.
        '''
        # Disable Blazegraph lookup
        config.DATABASE_EXISTING = False
        # Disable force Mongo Spfyid at specific value.
        config.DATABASE_BYPASS = False

        # Files and URIs for testing.
        g1 = GENOMES_LIST_ECOLI[0]
        g2 = GENOMES_LIST_ECOLI[1]
        hash1 = generate_hash(g1)
        hash2 = generate_hash(g2)
        uri1 = gu(':' + hash1)
        uri2 = gu(':' + hash2)

        r1, dup1 = _check(uri1)
        assert r1 == 0
        assert not dup1

        r2, dup2 = _check(uri2)
        assert r2 == 1
        assert r1 != r2
        assert not dup2

        r3, dup3 = _check(uri1)
        assert r3 == r1
        assert dup3
