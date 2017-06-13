import os
import tarfile
import zipfile
import json
import logging
import redis
from modules.loggingFunctions import initialize_logging
from flask import current_app
from werkzeug.utils import secure_filename
from rdflib import URIRef
from rq import Queue

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)

def handle_tar(filename, now):
    if tarfile.is_tarfile(filename):
        tar = tarfile.open(filename)
        extracted_dir = os.path.join(
            current_app.config['DATASTORE'] + '/' + now)
        os.mkdir(extracted_dir)
        for member in tar.getmembers():
            if not secure_filename(member.name):
                return 'invalid upload', 500
                # TODO: wipe temp data
        tar.extractall(path=extracted_dir)
        for fn in os.listdir(extracted_dir):
            os.rename(extracted_dir +'/' + fn, extracted_dir +'/'+ now + '-' + fn)
        tar.close()

        # set filename to dir for spfy call
        return extracted_dir

def handle_zip(filename,now):
    z = zipfile.ZipFile(filename,'r')
    extracted_dir = os.path.join(
        current_app.config['DATASTORE'] + '/' + now)
    os.mkdir(extracted_dir)
    for info in z.infolist():
        if not secure_filename(info.filename):
            return 'invalid upload', 500
    z.extractall(path=extracted_dir)
    for fn in os.listdir(extracted_dir):
        os.rename(extracted_dir +'/' + fn, extracted_dir +'/'+ now + '-' + fn)
    z.close()

    # set filename to dir for spfy call
    return extracted_dir

def fix_uri(s):
    '''
    Workaround: Flask's path converter allows slashes, but only a SINGLE slash.
    This adds the second slash.
    Also converts to rdflib.URIRef
    '''
    if 'http:/' in s:
        s = s.replace('http:/', 'http://')
    elif 'https:/' in s:
        s = s.replace('https:/', 'https://')
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
        if type(uris) is set:
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

def fetch_job(job_id):
    '''
    Iterates through all queues looking for the job.
    '''
    redis_url = current_app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    queues = current_app.config['QUEUES_SPFY']
    for queue in queues:
        q = Queue(queue, connection=redis_connection)
        job = q.fetch_job(job_id)
        if job is not None:
            return job
    return Job(is_failed=True, exc_info='job not found')

class Job(object):
    '''
    A class to mimick the Job object returned by RQ's Queue.fetch_job()
    We use this to create custom Jobs with our own error messages.
    This allows custom error messages to be parsed by the same code.
    '''
    def __init__(self, is_finished=False, result='', is_failed=False, exc_info=''):
        self.is_finished = is_finished
        self.result = result
        self.is_failed = is_failed
        self.exc_info = exc_info
