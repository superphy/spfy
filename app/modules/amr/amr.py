import subprocess
import os
import shutil

def amr(query_file):
    '''Call RGI on query_file and convert to tsv.
    '''
    # Main RGI call.
    # Note: -o will actually append .json to the filename.
    subprocess.check_call([
        'rgi',
        'main',
        '-i', query_file,
        '-o', query_file])

    # Generates the '.tsv' we want (RGI names as a '.txt').
    ext = query_file.split('.')[-1]
    rgi_json = query_file.strip(ext) + 'json'
    subprocess.check_call([
        'rgi',
        'tab',
        '-i', rgi_json])

    # Rename and move the tsv to the original directory, if applicable.
    amr_file = query_file + '_rgi.tsv'
    # RGI appends '.txt' to the full input filename, eg. .fasta.txt
    shutil.move(query_file+'.txt', amr_file)

    return amr_file
