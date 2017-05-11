import os
import tarfile
import zipfile
import json
from flask import current_app
from werkzeug.utils import secure_filename
from rdflib import URIRef

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
    elif 'https:/' in attributetype:
        s = s.replace('https:/', 'https://')
    uri = URIRef(s)
    return uri

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True
