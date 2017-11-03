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
