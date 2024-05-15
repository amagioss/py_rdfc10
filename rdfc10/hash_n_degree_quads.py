
import itertools
from rdflib import BNode
import rdfc10.commons as commons
from rdfc10.logger import logger
from rdfc10.hash_1_degree_quads import compute_first_degree_hash


def get_identifier(state: commons.Rdfc10State, issuer: commons.IDIssuer, related: str) -> str:
    if state.canonical_issuer.is_set(related):
        return f"_:{state.canonical_issuer.issueID(related)}"
    elif issuer.is_set(related):
        return f"_:{issuer.issueID(related)}"
    else:
        return compute_first_degree_hash(state, related)


#
# related is BNode id
def compute_hash_related_blank_node(state: commons.Rdfc10State, related: str, quad: commons.Quad,
                                    issuer: commons.IDIssuer, position: str) -> str:
    
    logger.debug(f"Entering compute_hash_related_blank_node with {related} {quad} {issuer} {position}")

    identifier = get_identifier(state, issuer, related)

    input_str = position 
    if input_str != "g":
        input_str = f"{input_str}<{quad.p.toPython()}>"

    input_str = f"{input_str}{identifier}"

    hash_str = commons.compute_hash(state.hash_algorithm, input_str)

    logger.debug(f"Hash_input {quad} {input_str} is {hash_str}")

    return hash_str


def update_hn(Hn: dict, hash_str: str, bnode_str: str):
    if not hash_str in Hn:
        Hn[hash_str] = [bnode_str]
    else:
        Hn[hash_str].append(bnode_str)
    return

def compute_n_degree_hash(state: commons.Rdfc10State, identifier: str, 
                          issuer: commons.IDIssuer) -> str:
    logger.debug(f"Computing n-degree hash for {identifier}")
    Hn = dict() 

    # Step 2, 3
    # Calculate a unique hash for all other bnodes that are immediately connected to 'identifier'
    # Note that this step will, in possible recursive calls, create additional steps for the "gossips"
    for quad in state.bnode_to_quads[identifier]:
        if isinstance(quad.s, BNode) and quad.s.toPython() != identifier:
            hash_str = compute_hash_related_blank_node(state, quad.s.toPython(), quad, issuer, "s")
            update_hn(Hn, hash_str, quad.s.toPython())
        elif isinstance(quad.o, BNode) and quad.o.toPython() != identifier:
            hash_str = compute_hash_related_blank_node(state, quad.o.toPython(), quad, issuer, "o")
            update_hn(Hn, hash_str, quad.o.toPython())
        else:
            pass

    hashes = sorted(Hn.keys())
    # Log Hn 
    for h in hashes:
        logger.debug(f"{h} -> {Hn[h]}")

    data_to_hash = ""
    for hash in hashes:
        data_to_hash = f"{data_to_hash}{hash}"
        chosen_path = "" 
        chosen_issuer = None

        bnodes = Hn[hash]
        permutations = list(itertools.permutations(bnodes))

        for p in permutations: 
            issuer_copy = issuer.copy()
            path = "" 
            recursion_list = []
            next_permutation = False 

            for related in p:
                if state.canonical_issuer.is_set(related):
                    path = f"{path}_:{state.canonical_issuer.issueID(related)}"
                else: 
                    if not issuer_copy.is_set(related):
                        recursion_list.append(related)
                    path = f"{path}_:{issuer_copy.issueID(related)}"

                if ((len(chosen_path) > 0) and (len(path) >= len(chosen_path)) and
                        (path > chosen_path)):
                    next_permutation = True
                    break 
            
            if next_permutation:
                continue

            for related in recursion_list:
                result = compute_n_degree_hash(state, related, issuer_copy)

                path = f"{path}_:{issuer_copy.issueID(related)}"

                path = f"{path}<{result[0]}>" # result[0] = hash

                issuer_copy = result[1]  # result[1] = issuer

                if ((len(chosen_path) > 0) and (len(path) >= len(chosen_path)) and
                        (path > chosen_path)):
                    next_permutation = True
                    break 
            if next_permutation:
                continue

            if ((len(chosen_path) == 0) or (path < chosen_path)):
                chosen_path = path
                chosen_issuer = issuer_copy
            
        data_to_hash = f"{data_to_hash}{chosen_path}"
        issuer = chosen_issuer

    hash = commons.compute_hash(state.hash_algorithm, data_to_hash)

    return (hash, issuer)


    


