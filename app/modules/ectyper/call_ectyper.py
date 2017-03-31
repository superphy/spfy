import shutil
import os
import logging
import subprocess
import cPickle as pickle
from ast import literal_eval
from os.path import basename
from app.modules.loggingFunctions import initialize_logging

log_file = initialize_logging()
log = logging.getLogger(__name__)

def call_ectyper(args_dict):
    # i don't intend to import anything from ECTyper (there are a lot of
    # imports in it - not sure if we'll use them all)
    # concurrency is handled at the batch level, not here (note: this might change)
    # we only use ectyper for serotyping and vf, amr is handled by rgi directly
    if not args_dict['disable_serotype'] or not args_dict['disable_vf']:

        #hack to allow ectyper to run in docker
        filepath=(args_dict['i'])
        wrapper_dir = os.path.dirname(os.path.abspath(__file__))
        # this temp file path is req for ectyper
        temp_file_path = os.path.join(wrapper_dir, 'temp.fna')
        shutil.copyfile(args_dict['i'], temp_file_path)
        args_dict['i']= temp_file_path
        log.debug(temp_file_path)

        ectyper_path = os.path.join(wrapper_dir, 'ecoli_serotyping/src/Tools_Controller/tools_controller.py')
        log.debug(ectyper_path)
        ectyper_dict = subprocess.check_output([ectyper_path,
                                                '-in', args_dict['i'],
                                                '-s', str(
                                                    int(not args_dict['disable_serotype'])),
                                                '-vf', str(
                                                    int(not args_dict['disable_vf'])),
                                                '-pi', str(args_dict['pi'])
                                                ])
        # removing that temp file we created
        os.remove(temp_file_path)

        # because we are using check_output, this catches any print messages from tools_controller
        # TODO: switch to pipes
        if 'error' in ectyper_dict.lower():
            log.fatal('ECTper failed for' + args_dict['i'])
            raise Exception('ECTper failed for' + filepath)

        ectyper_dict = literal_eval(ectyper_dict)

        # TODO: edit ectyper so we're not using this ducktape approach
        # we are calling tools_controller on only one file, so grab that dict
        key, ectyper_dict = ectyper_dict.popitem()

        p = os.path.join(filepath + '_ectyper.p')
        pickle.dump(ectyper_dict,open(p,'wb'))

    return p