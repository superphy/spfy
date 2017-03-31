#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

# use: python savvy.py -i samples/ANLJ01.1.fsa_nt

# S:erotype
# A:ntimicrobial Resistance
# V:irulence Factors
# -vy
# essentially implements the same pipeline as blob_savvy_enqueue() in spfy.py, but without the RQ backing and with option graph generation of outputs

import logging

from app.modules.qc.qc import qc
from app.modules.blazeUploader.reserve_id import write_reserve_id
from app.modules.ectyper.call_ectyper import call_ectyper
from app.modules.amr.amr import amr
from app.modules.amr.amr_to_dict import amr_to_dict
from app.modules.beautify.beautify import beautify
from app.modules.turtleGrapher.datastruct_savvy import datastruct_savvy
from app.modules.turtleGrapher.turtle_grapher import turtle_grapher
from app.modules.loggingFunctions import initialize_logging

log_file = initialize_logging()
log = logging.getLogger(__name__)

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
    log.info("pickled ectyper file: " + ectyper_p)

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

    savvy(args_dict)
