from modules.turtleGrapher.turtle_utils import generate_uri as gu

# this is used to determine whether to use :hasPart or :isFoundIn for searching the blazegraph db. We assign weights to each
weights = {gu(':spfyId'):0,
    gu('g:Genome'):1,
    gu('so:0001462'):2,
    gu('g:Contig'):3,
    gu('faldo:Position'):4,
    gu('faldo:Region'):5,
    gu(':Marker'):6, gu(':AntimicrobialResistanceGene'):6, gu('VirulenceFactor'):6}
