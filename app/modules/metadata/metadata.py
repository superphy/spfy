import pandas as pd
from rdflib import Graph
from werkzeug.utils import secure_filename
from modules.groupComparisons.logical_queries import resolve_spfyids
from modules.turtleGrapher.turtle_utils import generate_uri as gu
from modules.blazeUploader.upload_graph import upload_graph

d = {'Human': 'http://purl.bioontology.org/ontology/NCBITAXON/9606',
    'Bovine': 'http://purl.bioontology.org/ontology/NCBITAXON/9913'}

def upload_metadata(csv_file):
    df = pd.read_csv(csv_file)
    graph = Graph()
    for f in df.Filename:
        # resolve the spfyid for that file
        # note: we have to run secure_filename to replicate the same saved
        # name in the db
        spfyid = resolve_spfyids(gu('dc:description'), secure_filename(f))
        # check if a spfyid was found
        # Note: spfyid should be a Set
        if spfyid:
            # take the first (and only) spfyid
            sid = str(spfyid.pop())
            # grab the host
            host = df.Host[df.Filename==f]
            host = host.iloc[0]
            # add the host URI to the spfyID URI
            graph.add((gu(sid), gu('ge:0001567'), gu(d[host])))
    upload_graph(graph)
    return graph.serialize(format='json-ld')
