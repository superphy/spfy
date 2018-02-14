from middleware.models import SubtypingRow, SubtypingResult
from tests.constants import BEAUTIFY_VF_SEROTYPE

def test_models():
    subtyping_list = [
        SubtypingRow(
            analysis=d['analysis'],
            contigid=d['contigid'],
            filename=d['filename'],
            hitcutoff=str(d['hitcutoff']),
            hitname=d['hitname'],
            hitorientation=d['hitorientation'],
            hitstart=str(d['hitstart']),
            hitstop=str(d['hitstop'])
        )
    for d in BEAUTIFY_VF_SEROTYPE]
    subtyping_result = SubtypingResult(
        rows = subtyping_list
    )
    subtyping_result.validate()
