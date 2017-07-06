import os
import tarfile
import zipfile
import logging
from modules.loggingFunctions import initialize_logging
from flask import current_app
from werkzeug.utils import secure_filename
from rdflib import URIRef

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)

def handle_tar(filename, submission_folder):
    if tarfile.is_tarfile(filename):
        tar = tarfile.open(filename)
        for member in tar.getmembers():
            if not secure_filename(member.name):
                return 'invalid upload', 500
                # TODO: wipe temp data
        tar.extractall(path=submission_folder)
        tar.close()
        # set filename to dir for spfy call
        return submission_folder

def handle_zip(filename,submission_folder):
    z = zipfile.ZipFile(filename,'r')
    for info in z.infolist():
        if not secure_filename(info.filename):
            return 'invalid upload', 500
    z.extractall(path=submission_folder)
    z.close()
    # set filename to dir for spfy call
    return submission_folder

def fix_uri(s):
    '''
    Workaround: Flask's path converter allows slashes, but only a SINGLE slash.
    This adds the second slash.
    Also converts to rdflib.URIRef
    '''
    # we perform a check for a working URI because
    # sometimes the URI is pulled directly from the db
    # when we to tofromHumanReadable() decorator
    if 'http://' in s or 'https://' in s:
        return s
    elif 'http:/' in s:
        s = s.replace('http:/', 'http://')
    elif 'https:/' in s:
        s = s.replace('https:/', 'https://')
    else:
        raise Exception('Not sure why you are calling fix_uri() with a valid string')
    uri = URIRef(s)
    return uri

def to_readable(values,readable):
    '''
    Converts URI to human readable form.
    If you want the inverse, call this function with readable.inv
    Args:
        values: (list/set/string) of the value we want to convert
        readable: the bidict (this is a lib from pip). defined in blacklist.py
    '''
    st = set()
    if type(values) in (list, set):
        for value in values:
            try:
                st.add(readable[value])
            except:
                log.error('to_readable(): No readable form found for ' + value)
                st.add(value)
        if type(values) is set:
            return st
        else:
            return list(st)
    else:
        # sent me a single item
        try:
            return readable[values]
        except:
            log.error('to_readable(): No readable form found for ' + values)
            return values
