import os
import tarfile
import zipfile
from flask import current_app

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
