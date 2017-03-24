import os
from app.modules.qc.qc import qc

def test_modules_qc():
    for f in os.listdir('ecoli'):
        assert qc(f) == True
    for f in os.listdir('notEcoli'):
        assert qc(f) == False