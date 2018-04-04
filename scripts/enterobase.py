import os
import requests
import argparse
import json
import cPickle as pickle

from time import sleep

def get(identifier, barcode, dl_folder):
    f = requests.get('http://enterobase.warwick.ac.uk/upload/download?assembly_id=' + str(identifier) + '&database=ecoli')
    fn = dl_folder + '/' + str(barcode) + '.fasta'
    if not f.text == 'No Assembly or strain record found':
        with open(fn, 'w') as fl:
            fl.write(f.text)
            print('wrote ' + fn)

def _strains():
    p = 'strains.p'
    if os.path.isfile(p):
        strains = pickle.load(open(p,'rb'))
    else:
        options = {
            'no_legacy':'true',
            'experiment':'assembly_stats',
            'database':'ecoli',
            'strain_query_type':'query',
            'strain_query':'all'
        }
        r = requests.post('http://enterobase.warwick.ac.uk/get_data_for_experiment', data=options)
        d = r.json()
        # d.keys()
        # [u'strains', u'experiment']
        strains = d['strains']
        experiment = d['experiment']
        # >>> len(strains)
        # 54181
        # >>> len(experiment)
        # 53179
        # >>> strains[0]
        # {u'secondary_sample_accession': u'SRS1016187', u'comment': None, u'collection_year': 2009, u'serotype': None, u'antibiotic_resistance': None, u'strain': u'AZ-TG71511', u'postcode': None, u'owner': None, u'continent': u'North America', u'city': None, u'collection_date': None, u'collection_month': 10, u'not_editable': True, u'id': 7740, u'admin1': u'Illinois', u'source_details': u'packaged turkey', u'admin2': None, u'longitude': None, u'best_assembly': 21647, u'study_accession': u'PRJNA230968', u'serological_group': None, u'source_niche': u'Poultry', u'barcode': u'ESC_AA7740AA', u'latitude': None, u'simple_disease': None, u'secondary_study_accession': u'SRP038995', u'ecor': None, u'path_nonpath': None, u'disease': None, u'uberstrain': 7740, u'country': u'United States', u'release_date': u'2015-07-29', u'created': u'2015-08-27', u'Accession': [{u'seq_platform': u'ILLUMINA', u'seq_library': u'Paired', u'experiment_accession': u'SRX1123765', u'seq_insert': 500, u'accession': u'SRR2133399'}], u'assembly_status': u'Assembled', u'sample_accession': u'SAMN02463300', u'simple_pathogenesis': None, u'source_type': u'Avian', u'contact': u'FOOD AND DRUG ADMINISTRATION, CENTER FOR FOOD SAFETY AND APPLIED NUTRITION', u'species': u'Escherichia coli', u'collection_time': None}
        # >>> experiment[0]
        # {u'status': u'Assembled', u'barcode': u'ESC_CA1647AA_AS', u'n50': 113343, u'pipeline_version': 2.2, u'low_qualities': 10355, u'coverage': None, u'total_length': 4878259, u'id': 7740, u'contig_number': 157, u'top_species': u'Escherichia coli / Shigella;94.66%'}
        #df = pd.DataFrame.from_records(strains)
        # >>> df.keys()
        # Index([u'barcode', u'can_view', u'contig_number', u'coverage',
        #        u'extra_row_info', u'id', u'low_qualities', u'n50', u'pipeline_version',
        #        u'status', u'top_species', u'total_length'],
        #       dtype='object')

        # Retrive assembly barcode from experiment
        strains_len = len(strains)
        experiment_len = len(experiment)
        print("{} strains and {} experiment objects found".format(strains_len, experiment_len))
        print("Begin mapping assembly barcode")
        for index, row in enumerate(strains):
            print("Finding assembly barcode for {}/{} strains".format(index+1, strains_len))
            assembled = row['assembly_status']
            assembly_barcode=''
            if assembled == 'Assembled':
                id = row['id']
                for row2 in experiment:
                    if row2['id'] == id:
                        assembly_barcode = row2['barcode']
                if assembly_barcode == '':
                    raise Warning('no assembly barcode found')
            strains[index]['assembly_barcode'] = assembly_barcode
        print("Finish mapping assembly barcode")
        pickle.dump(strains, open(p, 'wb'))
        print("Modified strains file stored as strains.p")
    return strains

def enterobase(c=None):
    '''
    Downloads all the E.coli genomes from Enterobase.
    '''
    strains = _strains()
    dl_folder = 'enterobase_db'

    if not os.path.exists(dl_folder):
        os.makedirs(dl_folder)
    for row in strains:
        identifier = row['best_assembly']
        barcode = row['assembly_barcode']
        assembled = row['assembly_status']
        if assembled == 'Assembled':
            i = 1
            while i < 10:
                try:
                    get(identifier, barcode, dl_folder)
                    i = 10
                    # If a max # genomes was supplied.
                    if c and c==1:
                        return 0
                    elif c:
                        c -= 1
                except:
                    print('sleeping ' + str(i) + ' min')
                    sleep(60 * i)
                    i += 1
                    continue

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        help="# of Genomes to Download (default = all available).",
        required=False,
        type=int
    )
    args = parser.parse_args()

    enterobase(args.c)
