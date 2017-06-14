#import pytest

from routes.ra_posts import handle_singleton

# an example of the original jobs_dict with 2 files and both Serotype/VF
# and AMR options selected
jobs_dict = {
  "16515ba5-040d-4315-9c88-a3bf5bfbe84e": {
    "analysis": "Quality Control",
    "file": "/datastore/2017-06-14-21-26-43-375215-GCA_001683595.1_NGF2_genomic.fna"
  },
  "920a21f7-3fc2-4d63-b8b5-1014a981df08": {
    "analysis": "Antimicrobial Resistance",
    "file": "/datastore/2017-06-14-21-26-43-375215-GCA_001891695.1_ASM189169v1_genomic.fna"
  },
  "9b043d55-cb16-46bd-b086-d2a11c053b54": {
    "analysis": "Antimicrobial Resistance",
    "file": "/datastore/2017-06-14-21-26-43-375215-GCA_001683595.1_NGF2_genomic.fna"
  },
  "9c7b0aee-2d9c-4af5-83f2-bcd9e2369e80": {
    "analysis": "Virulence Factors and Serotype",
    "file": "/datastore/2017-06-14-21-26-43-375215-GCA_001891695.1_ASM189169v1_genomic.fna"
  },
  "9d2533d9-49cb-4a1f-baa8-109e9117d8ca": {
    "analysis": "ID Reservation",
    "file": "/datastore/2017-06-14-21-26-43-375215-GCA_001891695.1_ASM189169v1_genomic.fna"
  },
  "aa10aedc-c7c2-4fd9-8756-a907ea45382a": {
    "analysis": "ID Reservation",
    "file": "/datastore/2017-06-14-21-26-43-375215-GCA_001683595.1_NGF2_genomic.fna"
  },
  "c96619b8-b089-4a3a-8dd2-b09b5d5e38e9": {
    "analysis": "Virulence Factors and Serotype",
    "file": "/datastore/2017-06-14-21-26-43-375215-GCA_001683595.1_NGF2_genomic.fna"
  },
  "e8f72192-aae9-4859-ba9f-0c95ff480fb5": {
    "analysis": "Quality Control",
    "file": "/datastore/2017-06-14-21-26-43-375215-GCA_001891695.1_ASM189169v1_genomic.fna"
  }
}

def test_handle_singleton():
    r = handle_singleton(jobs_dict)
    print r
    assert True

if __name__ == "__main__":
    test_handle_singleton()
