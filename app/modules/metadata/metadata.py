import pandas as pd
from rdflib import Graph
from modules.groupComparisons.logical_queries import resolve_spfyids
from modules.turtleGrapher.turtle_utils import generate_uri as gu

d = {'Human': 'http://purl.bioontology.org/ontology/NCBITAXON/9606',
    'Bovine': 'http://purl.bioontology.org/ontology/NCBITAXON/9913'}

def metadata(csv_file):
    df = pd.read_csv(csv_file)
    graph = Graph()
    for f in df.Filename:
        # resolve the spfyid for that file
        spfyid = resolve_spfyids(gu('dc:description'), f)
        # check if a spfyid was found
        # Note: spfyid should be a Set
        if spfyid:
            # take the first (and only) spfyid
            sid = spfyid.pop()
            # grab the host
            host = df.Host[df.Filename==f]
            host = host.iloc[0]
            graph.add((sid, gu('ge:0001567'), gu(d[host])))
