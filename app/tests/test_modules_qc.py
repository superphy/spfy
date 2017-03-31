import os
from modules.qc.qc import qc

ecoli_dir = os.path.abspath('ecoli')
not_ecoli_dir = os.path.abspath('notEcoli')

def test_modules_qc():
    for f in ecoli_dir:
        assert qc(f) == True
    for f in not_ecoli_dir:
        assert qc(f) == False