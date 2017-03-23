import shutil
import os
import subprocess
import cPickle as pickle

from ast import literal_eval
from os.path import basename

def call_ectyper(args_dict):
    # i don't intend to import anything from ECTyper (there are a lot of
    # imports in it - not sure if we'll use them all)
    ectyper_dict = {}
    # concurrency is handled at the batch level, not here (note: this might change)
    # we only use ectyper for serotyping and vf, amr is handled by rgi directly
    if not args_dict['disable_serotype'] or not args_dict['disable_vf']:

        #hack to allow ectyper to run in docker
        filepath=(args_dict['i'])
        shutil.copyfile(args_dict['i'], '/app/tmp/temp.fna')
        args_dict['i']= 'tmp/temp.fna'

        ectyper_dict = subprocess.check_output(['./ecoli_serotyping/src/Tools_Controller/tools_controller.py',
                                                '-in', args_dict['i'],
                                                '-s', str(
                                                    int(not args_dict['disable_serotype'])),
                                                '-vf', str(
                                                    int(not args_dict['disable_vf'])),
                                                '-pi', str(args_dict['pi'])
                                                ])

        # because we are using check_output, this catches any print messages from tools_controller
        # TODO: switch to pipes
        if 'error' in ectyper_dict.lower():
            #logging.error('ectyper failed for' + args_dict['i'])
            print 'ECTyper failed for: ', filepath
            print 'returning graph w/o serotype'
            raise

        ectyper_dict = literal_eval(ectyper_dict)

        # TODO: edit ectyper so we're not using this ducktape approach
        # we are calling tools_controller on only one file, so grab that dict
        key, ectyper_dict = ectyper_dict.popitem()

        p = os.path.join(filepath + '_ectyper.p')
        pickle.dump(ectyper_dict,open(p,'wb'))

    return p
