import shutil
import os
import logging
import subprocess
import cPickle as pickle
import tempfile
import pandas as pd
from ast import literal_eval
from os.path import basename
from modules.loggingFunctions import initialize_logging
from middleware.modellers import model_serotype
from middleware.models import dump

log_file = initialize_logging()
log = logging.getLogger(__name__)

def call_ectyper_vf(args_dict):
    """ Use the old version of ECTyper at `superphy` for VF.
    """
    # Init return.
    p = 'no pickle'

    if args_dict['options']['vf']:
        # Workaround to allow ECTYPER to run in Docker.
        filepath=(args_dict['i'])
        wrapper_dir = os.path.dirname(os.path.abspath(__file__))
        # This temp file path is required for ectyper.
        temp = tempfile.NamedTemporaryFile()
        # Copy the actual genome file into the tempfile.
        shutil.copyfile(args_dict['i'], temp.name)
        # Create a copy of args_dict and update with the tempfile.
        args_dict = dict(args_dict)
        args_dict['i']= temp.name
        log.debug(temp.name)

        ectyper_path = os.path.join(wrapper_dir, 'ecoli_serotyping/src/Tools_Controller/tools_controller.py')
        log.debug(ectyper_path)
        ectyper_dict = subprocess.check_output([ectyper_path,
                                                '-in', args_dict['i'],
                                                '-s', str(
                                                    int(args_dict['options']['serotype'])),
                                                '-vf', str(
                                                    int(args_dict['options']['vf'])),
                                                '-pi', str(args_dict['pi'])
                                                ])
        # Removing that temp file we created.
        temp.close()

        # Because we are using check_output, this catches any print messages
        # from tools_controller.
        # TODO: switch to pipes
        if 'error' in ectyper_dict.lower():
            log.fatal('ECTper failed for' + args_dict['i'])
            raise Exception('ECTyper VF failed for' + filepath)

        ectyper_dict = literal_eval(ectyper_dict)

        # See #317
        if len(ectyper_dict.keys()) == 1:
            # This is the normal case where the key is the filename.
            key, ectyper_dict = ectyper_dict.popitem()
        else:
            # This is a bug when there is no filename mapping.
            td = {}
            for k in ectyper_dict:
                l = ectyper_dict[k]['Virulence Factors'].values()
                if l:
                    td[k] = l[0]
            ectyper_dict = {
                'Virulence Factors': td
            }
    
        
        assert isinstance(ectyper_dict, dict)
        # TODO: convert this to a VF model.
        # Path for the pickle dump.
        p = filepath + '_ectyper_vf.p'
        dump(ectyper_dict, p)

    return p

def call_ectyper_serotype(args_dict, pickle=True):
    """Use the new version of ECTyper at `master` for serotyping.
    """
    genome_file = args_dict['i']
    pi = str(args_dict['pi']) # Cast to str to execvp() in subprocess().
    pl = '50' # This is the default in ECTyper.
    output_dir = tempfile.mkdtemp()
    ret_code = subprocess.call([
        "ectyper",
        "-i",
        genome_file,
        "-d", # Percent Identity
        pi,
        "-l", # Percent Length
        pl,
        "-o",
        output_dir
    ])
    if ret_code == 0:
        output_file = os.path.join(output_dir, 'output.csv')
        # Create a SubtypingResult model from the output.
        subtyping_result = model_serotype(
            pi=pi,
            pl=pl,
            output_file=output_file
        )
        if pickle:
            # Path for the pickle dump.
            p = genome_file + '_ectyper_serotype.model'
            dump(subtyping_result, p)
            return p
        else:
            return subtyping_result
    else:
        raise Exception('ECTyper Serotyping failed for' + genome_file)
