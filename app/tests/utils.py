import os

def listdir_fullpath(d):
    '''Utility function to generate full path (still relative to root, not
    absoulte) for files in directories
    '''
    valid_extensions = ('.fasta', '.fna', '.fsa')
    l = []
    for f in os.listdir(d):
        filename, file_extension = os.path.splitext(f)
        if file_extension in valid_extensions:
            l.append(os.path.join(d, f))
    return l
