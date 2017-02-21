def spit_to_json(spit_dict):
    json_return = []
    # key is the full spfyURL
    for key in spit_dict:
        contig_instance = {}
        # in some contexts, the spfyID is refered to as the uriIsolate
        contig_instance['spfyID']=key
        contig_instance['genomeID']=spit_dict[key]['identifiers']['uriGenome']
        contig_instance['']
