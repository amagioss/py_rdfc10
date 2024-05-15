
from rdflib import BNode    
import rdflib
import rdfc10.commons as commons


def _modify_bnode_for_hashing(bnode: rdflib.IdentifiedNode, reference_bnode_id: str) -> BNode :
    if isinstance(bnode, BNode):
        if bnode.toPython() == reference_bnode_id:
            return BNode('a')
        else: 
            return BNode('z')
    else:
        return bnode


def compute_first_degree_hash(state: commons.Rdfc10State, reference_bnode_id: str):
    quads = state.bnode_to_quads.get(reference_bnode_id, [])
    mquads = []
    for q in quads: 
        mq_tuple = (_modify_bnode_for_hashing(q.s, reference_bnode_id).n3(),
                    q.p.n3(),
                    _modify_bnode_for_hashing(q.o, reference_bnode_id).n3())
        mq_tuple = " ".join(mq_tuple) + " ."
        mquads.append(mq_tuple)

    mquads.sort()
    concat_quads = '\n'.join(mquads) + "\n"

    # create a hex digest of the concatenated quads
    hash_digest = commons.compute_hash(state.hash_algorithm, concat_quads)
    return hash_digest
