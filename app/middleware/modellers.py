# We try to keep all model creation in this file so it's easier to reference.
import pandas as pd
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
        subtyping_list
    )

    return subtyping_result
