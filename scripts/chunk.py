def gather(directory):
    '''
    Gathers the geneome files in a given directory.
    '''
    import os
    list_files = []
    for root, dirs, files in os.walk(os.path.abspath(directory)):
        for file in files:
            if os.path.splitext(file)[1] in ('.fna', '.fasta'):
                list_files.append(os.path.join(root, file))
    print('# of files:', len(list_files))
    return list_files

def chunk(chunk_size, lst, f_base=''):
    import cPickle as pickle
    p = 0
    while p < len(lst):
        if p+chunk_size >= len(lst):
            q = len(lst)
        else:
            q = p + chunk_size
        f = '{f_base}batch_{p}_{q}.p'.format(f_base=f_base,p=p,q=q)
        l = lst[p:q]
        print 'writing pickle: ' + f
        pickle.dump(l,open(f,'wb'))
        p = q

def copy(p, dst):
    import shutil
    import cPickle as pickle
    from os.path import basename, join
    l = pickle.load(open(p, 'rb'))
    for f in l:
        # check for blank spaces in filename
        if any(substring in f for substring in (' ', '(',')')):
            fixed_fname = f
            for s in (' ', '(', ')'):
                fixed_fname = fixed_fname.replace(s,'_')
            dst_f = join(dst, basename(fixed_fname))
            print('problem character detected, copying: ' + f + ' as ' + dst_f)
            shutil.copy2(f, dst_f)
        else:
            print 'copying {0} to {1}'.format(f,dst)
            shutil.copy(f,dst)

if __name__ == '__main__':
    import argparse

    # parsing cli-input
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        help="Source of genome files",
        required=False,
        default='/Warehouse/Users/claing/enterobase_db-fixed'
    )
    parser.add_argument(
        "-n",
        help="Chunk size",
        required=False,
        default=3155
    )
    parser.add_argument(
        "-c",
        help="Location of a pickled chunk file",
        required=False
    )
    parser.add_argument(
        "-d",
        help="Destination for files",
        required=False
    )
    args = parser.parse_args()
    if args.c:
        print 'chunk file {0} provided, only moving...'.format(args.c)
        copy(args.c,args.d)
    else:
        print 'no chunk file provided, only creating chunks...'
        lst = gather(args.s)
        chunk(args.n, lst)
