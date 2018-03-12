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
        {
            'analysis':'Serotype',
            'contigid':'n/a',
            'filename':actual_filename(row['genome']),
            'hitcutoff':str(pi),
            'hitname':"{0}:{1}".format(row['O_prediction'],row['H_prediction']),
            'hitorientation':'n/a',
            'hitstart':'n/a',
            'hitstop':'n/a',
            'probability':'n/a'
        }
    for index, row in df.iterrows()]

    # Convert the list of rows into a SubtypingResult model.
    # subtyping_result = SubtypingResult(
    #     rows = subtyping_list
    # )
    assert subtyping_list
    assert subtyping_list[0]
    return subtyping_list

def model_vf(lst):
    """
    Casts the output from display.beautify into a SubtypingResult object.
    """
    # Type check.
    assert isinstance(lst, list)
    assert isinstance(lst[0], dict)
    print("model_vf() called with type {0} containing {1}".format(type(lst), str(lst)))
    subtyping_list = [
        {
            'analysis':item['analysis'],
            'contigid':item['contigid'],
            'filename':item['filename'],
            'hitcutoff':item['hitcutoff'],
            'hitname':item['hitname'],
            'hitorientation':item['hitorientation'],
            'hitstart':item['hitstart'],
            'hitstop':item['hitstop'],
            'probability':'n/a'
        }
    for item in lst]
    # Convert the list of rows into a SubtypingResult model.
    # subtyping_result = SubtypingResult(
    #     rows = subtyping_list
    # )
    return subtyping_list

def model_phylotyper(lst):
    """
    Casts phylotyper's return to the same format as VF/Serotyping.
    """
    phylotyper_list = [
        {
            'analysis':d['subtype_gene'],
            'contigid':d['contig'],
            'filename':d['genome'],
            'hitcutoff':'n/a',
            'hitname':d['subtype'],
            'hitorientation':'n/a',
            'hitstart':d['start'],
            'hitstop':d['stop'],
            'probability':d['probability']
        }
    for d in lst]

    return phylotyper_list
