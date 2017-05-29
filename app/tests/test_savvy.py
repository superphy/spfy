import os
import pytest
from modules.savvy import mock_reserve_id, get_spfyid_file

def test_mock_reserve_id():
    f = get_spfyid_file()
    if os.path.isfile(f):
        # you already have a spfyid file
        # this isn't the case in a test env, but may be true if tests are run after using savvy.py
        with open(f) as fl:
            spfyid = fl.read()
            spfyid = int(spfyid)
        # in the case that savvy.py was previously used (and tests may be running in a production env)
        # therefore, we don't call mock_reserve_id() directly as it'll overwrite their file
        assert spfyid > 0
    else:
        # this is the expected test env where the spfyid file doesn't exist
        # first call returns 1 as the id
        assert mock_reserve_id() = 1
        # second call should have incremented the stored file
        assert mock_reserve_id() = 2
