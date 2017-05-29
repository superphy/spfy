#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

# use: python -m modules.savvy -i /home/kevin/Desktop/nonGenBankEcoli/ECI-2866_lcl.fasta

# S:erotype
# A:ntimicrobial Resistance
# V:irulence Factors
# -vy
# essentially implements the same pipeline as blob_savvy_enqueue() in spfy.py, but without the RQ backing
# still graphs the results, so must have blazegraph running and defined in app/config.py

import os
import logging
import tempfile
from modules.qc.qc import qc
from modules.blazeUploader.reserve_id import write_reserve_id
from modules.ectyper.call_ectyper import call_ectyper
from modules.amr.amr import amr
from modules.amr.amr_to_dict import amr_to_dict
from modules.beautify.beautify import beautify
from modules.turtleGrapher.datastruct_savvy import datastruct_savvy
from modules.turtleGrapher.turtle_grapher import turtle_grapher
from modules.loggingFunctions import initialize_logging

log_file = initialize_logging()
log = logging.getLogger(__name__)

def get_spfyid_file():
    '''
    Uses tempfile to store the spfyid file on disk.
    We use a mmethod so the tests can access just the file as well.
    '''
    f = os.path.join(tempfile.gettempdir(), 'spfyid_count.txt')
    return f

def mock_reserve_id():
    '''
    Mocks the presence of Blazegraph to generate spfyids.
    '''
    f = get_spfyid_file()
    log.debug('spfyid_count file returned was : ' + f)
    # check if an existing spfyid count exists
    if os.path.isfile(f):
        with open(f) as fl:
            spfyid = fl.read()
            spfyid = int(spfyid)
    else:
        spfyid = 0
    # we assumed the spfyid in the file is already used
    spfyid += 1
    with open(f, 'w') as fl:
        fl.write(str(spfyid))
    return spfyid

def savvy(args_dict):
    '''

    '''
    log.info("Starting savvy.py from savvy(). Logfile is: " + str(log_file))
    log.debug("args_dict received was: " + str(args_dict))

    query_file = args_dict['i']
    log.info("query_file is: " + query_file)

    # (1) QC Step:
    qc_pass = qc(query_file)
    assert qc(query_file) == True
    log.info("QC: " + str(qc_pass))

    # (2) SpfyID Step:
    id_file = write_reserve_id(query_file)
    log.info("id_file:" + id_file)

    # (3) ECTyper Step:
    ectyper_p = call_ectyper(args_dict)
    log.info("Pickled ECTyper File: " + ectyper_p)

    # (4) ECTyper Beautify Step:
    ectyper_beautify = beautify(args_dict, ectyper_p)
    log.debug('Beautified ECTyper Result: ' + str(ectyper_beautify))

    # (5) Graphing ECTyper Result & Upload Step:
    ectyper_upload = datastruct_savvy(query_file, query_file + '_id.txt', query_file + '_ectyper.p')
    log.info('Graph & Upload of ECTyper Result: ' + ectyper_upload)

    # (6) RGI Step:
    amr_results_file = amr(query_file)
    log.info("AMR Results File: " + amr_results_file)

    # (7) AMR Results to Dictionary Step:
    amr_p = amr_to_dict(amr_results_file)
    log.info("Pickled AMR Results File: " + amr_p)

    # (8) AMR Beautify Step:
    amr_beautify = beautify(args_dict, amr_p)
    log.debug('Beautified AMR Result: ' + str(amr_beautify))

    # (9) Graping AMR Result & Upload Step:
    amr_upload = datastruct_savvy(query_file, query_file + '_id.txt', query_file + '_rgi.tsv_rgi.p')
    log.info('Graph & Upload of AMR Result: ' + amr_upload)

    # (10) Base Graphing & Upload Step:
    base_turtle_upload = turtle_grapher(query_file)
    log.info('Graph & Upload of Base Genome Data: ' + base_turtle_upload)

if __name__ == "__main__":
    import argparse

    log.info("Starting savvy.py from if __name__=='__main__'. Logfile is: " + str(log_file))

    # parsing cli-input
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        help="FASTA file",
        required=True
    )
    parser.add_argument(
        "--disable-serotype",
        help="Disables use of the Serotyper. Serotyper is triggered by default.",
        action="store_true"
    )
    parser.add_argument(
        "--disable-vf",
        help="Disables use of ECTyper to get associated Virulence Factors. VFs are computed by default.",
        action="store_true"
    )
    parser.add_argument(
        "--disable-amr",
        help="Disables use of RGI to get Antimicrobial Resistance Factors.  AMR genes are computed by default.",
        action="store_true"
    )
    parser.add_argument("--pi",
                        type=int,
                        help="Percentage of identity wanted to use against the database. From 0 to 100, default is 90%.",
                        default=90, choices=range(0, 100))
    args = parser.parse_args()
    # we make a dictionary from the cli-inputs and add are uris to it
    # mainly used for when a func needs a lot of the args
    args_dict = vars(args)

    # check/convert file to abspath
    args_dict['i'] = os.path.abspath(args_dict['i'])

    # add nested dictionary to mimick output from spfy web-app
    spfy_options = {'vf': not args_dict['disable_vf'], 'amr': not args_dict['disable_amr'], 'serotype': not args_dict['disable_serotype']}
    # the 'options' field represents things the user (of the web-app) has chosen to display, we still run ALL analysis on their files so their choices are not added to module calls (& hence kept separate)
    args_dict['options'] = spfy_options

    savvy(args_dict)
