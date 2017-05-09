import requests

def from_ebi_api(uri):
    API_ROOT = "https://www.ebi.ac.uk/ols/api/select?q="
    r = requests.get(API_ROOT + uri)
    data = r.json()
    label = data['response']['docs'][0]['label']
    return label

def human_readable(uris):
    '''
    Takes some collection of or a single uri and tries to grab humnan readable labels from https://www.ebi.ac.uk/ols/index.
    Return type identical to query type.
    '''
    if type(uris) in (set, list):
        st = set()
        for uri in uris:
            try:
                st.add(from_ebi_api(uri))
            except:
                st.add(uri)
        if type(uris) is set:
            return st
        else:
            return list(st)
    else:
        try:
            return from_ebi_api(uris)
        except:
            return uris

if __name__ == "__main__":
    all_types = [
      "http://purl.obolibrary.org/obo/GENEPIO_0001076",
      "http://purl.obolibrary.org/obo/GENEPIO_0001077",
      "https://www.github.com/superphy#VirulenceFactor",
      "http://purl.org/dc/elements/1.1/identifier",
      "https://www.github.com/superphy#AntimicrobialResistanceGene",
      "http://biohackathon.org/resource/faldo#Begin",
      "http://www.biointerchange.org/gfvo#Identifier",
      "http://biohackathon.org/resource/faldo#ExactPosition",
      "https://www.github.com/superphy#isFoundIn",
      "http://biohackathon.org/resource/faldo#Reference",
      "http://biohackathon.org/resource/faldo#Position",
      "http://biohackathon.org/resource/faldo#End",
      "http://www.w3.org/1999/02/22-rdf-syntax-ns#List",
      "https://www.github.com/superphy#Marker",
      "http://www.biointerchange.org/gfvo#DNASequence",
      "http://biohackathon.org/resource/faldo#Region",
      "http://www.w3.org/2000/01/rdf-schema#domain",
      "https://www.github.com/superphy#hasPart",
      "http://biohackathon.org/resource/faldo#ReverseStrandPosition",
      "http://purl.org/dc/elements/1.1/description",
      "http://www.w3.org/2000/01/rdf-schema#Class",
      "http://www.w3.org/2000/01/rdf-schema#subPropertyOf",
      "http://www.w3.org/2000/01/rdf-schema#Datatype",
      "http://www.w3.org/2002/07/owl#ObjectProperty",
      "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
      "http://www.biointerchange.org/gfvo#Description",
      "http://www.w3.org/2002/07/owl#TransitiveProperty",
      "https://www.github.com/superphy#spfyId",
      "http://www.w3.org/2000/01/rdf-schema#subClassOf",
      "http://purl.obolibrary.org/obo/SO_0001462",
      "http://www.biointerchange.org/gfvo#Contig",
      "http://www.w3.org/2000/01/rdf-schema#Resource",
      "http://www.biointerchange.org/gfvo#Genome",
      "http://www.w3.org/2000/01/rdf-schema#range",
      "http://purl.org/dc/elements/1.1/date",
      "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
    ]
    attribute_types = [
      "http://www.biointerchange.org/gfvo#Description",
      "http://www.biointerchange.org/gfvo#DNASequence",
      "http://www.biointerchange.org/gfvo#Identifier",
      "https://www.github.com/superphy#hasPart",
      "https://www.github.com/superphy#isFoundIn",
      "http://biohackathon.org/resource/faldo#Position",
      "http://purl.obolibrary.org/obo/GENEPIO_0001076",
      "http://purl.obolibrary.org/obo/GENEPIO_0001077",
      "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
      "http://www.w3.org/2000/01/rdf-schema#domain",
      "http://www.w3.org/2000/01/rdf-schema#range",
      "http://www.w3.org/2000/01/rdf-schema#subClassOf",
      "http://www.w3.org/2000/01/rdf-schema#subPropertyOf",
      "http://purl.org/dc/elements/1.1/description",
      "http://purl.org/dc/elements/1.1/date",
      "http://purl.org/dc/elements/1.1/identifier"
    ]
    print human_readable(attribute_types)
    print human_readable(all_types)
