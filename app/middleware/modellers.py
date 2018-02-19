# We try to keep all model creation in this file so it's easier to reference.
import pandas as pd
from middleware.models import SubtypingRow, SubtypingResult
from middleware.graphers.turtle_utils import actual_filename


def model_serotype(pi, pl, output_file):
    """
    Creates a SubtypingResult model from ECTYper's serotyping output.
    """
    # Read the vanilla output_file from ECTyper.
    df = pd.read_csv(output_file)

    # TODO: incorporate the pl.

    # Loop.
    subtyping_list = [
        SubtypingRow(
            analysis='Serotype',
            contigid='n/a',
            filename=actual_filename(row['genome']),
            hitcutoff=str(pi),
            hitname="{0}:{1}".format(row['O_prediction'],row['H_prediction']),
            hitorientation='n/a',
            hitstart='n/a',
            hitstop='n/a'
        )
    for index, row in df.iterrows()]

    # Convert the list of rows into a SubtypingResult model.
    subtyping_result = SubtypingResult(
        rows = subtyping_list
    )
    return subtyping_result

def model_vf(json_r):
    """
    Casts the output from display.beautify into a SubtypingResult object.
    """
    # Type check.
    assert isinstance(json_r, list)
    print("model_vf() called with type {0} containing {1}".format(type(json_r), str(json_r)))
    subtyping_list = [
        SubtypingRow(
            analysis=item('analysis'),
            contigid=item['contigid'],
            filename=item['filename'],
            hitcutoff=item['hitcutoff'],
            hitname=item['hitname'],
            hitorientation=item['hitorientation'],
            hitstart=item['hitstart'],
            hitstop=item['hitstop']
        )
    for item in json_r]
    # Convert the list of rows into a SubtypingResult model.
    subtyping_result = SubtypingResult(
        rows = subtyping_list
    )
    return subtyping_result
