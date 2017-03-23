import os

# our own slightly more general stuff
from app.modules.turtleGrapher.turtle_utils import generate_uri as gu, generate_hash

from app.config import database
from multiprocessing import Pool, cpu_count

def spfyids_single(args_dict):

    # this is temporary, TODO: include a spqarql query to the db
    uriIsolate = gu(':spfy' + str(database['count']))

    uriGenome = gu(':' + generate_hash(args_dict['i']))

    args_dict['uriIsolate'] = uriIsolate
    args_dict['uriGenome'] = uriGenome

    return args_dict


def hash_me(file_dict):
    uris = {}
    uris[file_dict['basename']] = {}
    uris[file_dict['basename']]['uriIsolate'] = gu(
        ':spfy' + str(file_dict['count']))
    uris[file_dict['basename']]['uriGenome'] = gu(
        ':' + generate_hash(file_dict['withpath']))
    return uris


def spfyids_directory(args_dict):
    '''
    TODO: make the database count actually work
    This is meant to preallocate spfyIDs
    -note may have problems with files that fail (gaps in id range)
    TODO: fix that^
    TODO: make this whole thing less messy
    '''


    print 'Precomputing hashes for all files in directory, may take awhile...'

    files = os.listdir(args_dict['i'])
    count = database['count']

    # inital mapping of a files to a number(spfyID)
    files_list = []
    for f in files:
        file_dict = {}
        file_dict['basename'] = f
        file_dict['withpath'] = args_dict['i'] + f
        file_dict['count'] = count
        files_list.append(file_dict)
        count += 1
    # TODO: write-out count

    # hasing and make uris
    p = Pool(cpu_count())
    # this will return a list of dicts
    uris = p.map(hash_me, files_list)

    # convert the list of dicts into a nested dict structure {filename:
    # {'uriIsolate' , 'uriGenome'}}
    # ducttape soln
    uris_dict = {}
    for uri_dict in uris:
        uris_dict[uri_dict.keys()[0]] = uri_dict.values()[0]

    args_dict['uris'] = uris_dict

    return args_dict

def ids(args_dict):
    # check if a directory was passed or a just a single file
    # updates args_dict with appropriate rdflib.URIRef's
    if os.path.isdir(args_dict['i']):
        if args_dict['i'][-1] is not '/':
            args_dict['i'] = args_dict['i'] + '/'
        args_dict = spfyids_directory(args_dict)
    else:
        args_dict = spfyids_single(args_dict)