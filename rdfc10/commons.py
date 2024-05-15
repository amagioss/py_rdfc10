
import rdflib 
import hashlib
from typing import Dict, List
from dataclasses import dataclass
from typing import NamedTuple


# create a NamedTuple type for quads
Quad = NamedTuple('Quad', [('s', rdflib.IdentifiedNode), 
                           ('p', rdflib.IdentifiedNode),
                           ('o', rdflib.IdentifiedNode)])

class IDIssuer: 
    def __init__(self, prefix="c14n"): 
        self.id_counter = 0
        self.id_prefix = prefix
        self.issued_ids_map : Dict[str, str] = dict()

    def issueID(self, bnode: str):
        if bnode in self.issued_ids_map:
            return self.issued_ids_map[bnode]
        self.issued_ids_map[bnode] = f"{self.id_prefix}{self.id_counter}"
        self.id_counter += 1
        return self.issued_ids_map[bnode]
    
    def map(self, bnode: str):
        return self.issued_ids_map.get(bnode, None)
    
    def is_set(self, bnode: str):
        return bnode in self.issued_ids_map
    
    def copy(self):
        new_issuer = IDIssuer()
        new_issuer.id_counter = self.id_counter
        new_issuer.id_prefix = self.id_prefix
        new_issuer.issued_ids_map = self.issued_ids_map.copy()
        return new_issuer
    
    # Create an iterator that will return (key, value) coorespondig to the issued_ids_map
    def __iter__(self):
        return iter(self.issued_ids_map.items())
    
@dataclass
class Rdfc10State:
    bnode_to_quads: Dict[str, List[Quad]]
    hash_to_bnodes: dict
    canonical_issuer: IDIssuer
    hash_algorithm: str


def compute_hash(hash_algo, input: str):
    hash_inst = hashlib.new(hash_algo)
    hash_inst.update(input.encode())
    hash_digest = hash_inst.hexdigest()
    return hash_digest
