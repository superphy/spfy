import shutil
import subprocess

from ast import literal_eval


from app.modules.turtleGrapher import datastruct_savvy
from app.modules.amr.amr import generate_amr

def call_ectyper(graph, args_dict):
    # i don't intend to import anything from ECTyper (there are a lot of
    # imports in it - not sure if we'll use them all)



    ectyper_dict = {}
    #logging.info('calling ectyper from fun call_ectyper')
    # concurrency is handled at the batch level, not here (note: this might change)
    # we only use ectyper for serotyping and vf, amr is handled by rgi directly
    if not args_dict['disable_serotype'] or not args_dict['disable_vf']:

        #hack to allow ectyper to run in docker
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
        #logging.info('inner call completed')

        # because we are using check_output, this catches any print messages from tools_controller
        # TODO: switch to pipes
        if 'error' in ectyper_dict.lower():
            #logging.error('ectyper failed for' + args_dict['i'])
            print 'ECTyper failed for: ', args_dict['i']
            print 'returning graph w/o serotype'
            return graph

        #logging.info('evalulating ectyper output')
        # generating the dict
        ectyper_dict = literal_eval(ectyper_dict)
        # logging.info(ectyper_dict)
        #logging.info('evaluation okay')

        # TODO: edit ectyper sure were not using this ducktape approach
        # we are calling tools_controller on only one file, so grab that dict
        key, ectyper_dict = ectyper_dict.popitem()

        if not args_dict['disable_serotype']:
            # serotype parsing
            #logging.info('parsing Serotype')
            graph = datastruct_savvy.parse_serotype(
                graph, ectyper_dict['Serotype'], args_dict['uriIsolate'])
            #logging.info('serotype parsed okay')

        if not args_dict['disable_vf']:
            # vf
            #logging.info('parsing vf')
            graph = datastruct_savvy.parse_gene_dict(
                graph, ectyper_dict['Virulence Factors'], args_dict['uriGenome'])
            #logging.info('vf parsed okay')

    if not args_dict['disable_amr']:
        # amr
        #logging.info('generating amr')
        amr_result = generate_amr(
            graph, args_dict['uriGenome'], args_dict['i'])
        graph = amr_result['graph']
        ectyper_dict['Antimicrobial Resistance'] = amr_result['amr_dict']
        #logging.info('amr generation okay')

    return {'graph': graph, 'ectyper_dict': ectyper_dict}
