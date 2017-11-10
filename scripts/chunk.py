def chunk(chunk_size, lst, f_base='/'):
    import cPickle as pickle
    p = 0
    while p < len(lst):
        if p+chunk_size >= len(lst):
            q = len(lst)
        else:
            q = p + chunk_size
        f = '{f_base}batch_{p}_{q}.p'.format(f_base=f_base,p=p,q=q)
        l = lst[p:q]
        pickle.dump(l,open(f,'wb'))
        p = q

def move(p, dst):
    import shutil
    import cPickle as pickle
    from os.path import basename, join
    l = pickle.load(open(p, 'rb'))
    for f in l:
        # check for blank spaces in filename
        if ' ' in f:
            b = basename(f)
            dst_f = join(dst, f.replace(' ','_'))
            print('blank space detected, copying: ' + f + ' as ' + dst_f)
            shutil.copy2(src, dst_f)
        else:
            shutil.copy(f,dst)
