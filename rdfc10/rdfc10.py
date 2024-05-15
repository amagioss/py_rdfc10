
import rdflib 
from rdflib import Graph, BNode
from rdfc10.logger import logger
import rdfc10.commons as commons
import rdfc10.hash_n_degree_quads as hash_n_degree_quads
from rdfc10.hash_1_degree_quads import compute_first_degree_hash
    
class Rdfc10:
    def __init__(self):
        self.state = commons.Rdfc10State(dict(), dict(), commons.IDIssuer(), hash_algorithm='sha256')

    def init_bnode_to_quads(self, g: Graph):
        for s, p, o in g.triples((None, None, None)):
            quad = commons.Quad(s, p, o)
            if isinstance(s, BNode):
                s = s.toPython()
                if s not in self.state.bnode_to_quads:
                    self.state.bnode_to_quads[s] = []
                self.state.bnode_to_quads[s].append(quad)
            if isinstance(o, BNode):
                o = o.toPython()
                if o not in self.state.bnode_to_quads:
                    self.state.bnode_to_quads[o] = []
                self.state.bnode_to_quads[o].append(quad)

    # Step 3
    # Compute a hash value for each bnode (depending on the quads it appear in)
    # In simple cases a hash value refers to one bnode only; in unlucky cases there
    # may be more. Hence the usage of the hash_to_bnodes map.
    def hash_first_degree(self):
        for bnode in self.state.bnode_to_quads.keys():
            hash_val = compute_first_degree_hash(self.state, bnode)
            if hash_val not in self.state.hash_to_bnodes:
                self.state.hash_to_bnodes[hash_val] = []
            self.state.hash_to_bnodes[hash_val].append(bnode)

    # Step 4
    # For each hash, take the corresponding bnode and issue a new, canonical id in a sequence.
    # This only works for those hashes where there is one associated bnode. For the ones
    # where this is not the case, step 5 will kick in later.
    # It is important to order the hashes, because it influences the order of issuing the canonical ids.
    # If a bnode is "handled", i.e., it does have a canonical ID, it is removed from the
    # state structure on hash->bnodes.
    def issue_canonical_ids(self):
        hash_vals = list(self.state.hash_to_bnodes.keys())
        hash_vals.sort()
        for hash_val in hash_vals:
            bnodes = self.state.hash_to_bnodes[hash_val]
            if len(bnodes) == 1:
                bnode = bnodes[0]
                canon_id = self.state.canonical_issuer.issueID(bnode)
                logger.debug(f"Canonical ID for {bnode} is {canon_id}")
                del self.state.hash_to_bnodes[hash_val]


    # Step 5
    # This step takes care of the bnodes that do not have been canonicalized in the previous step, 
    # because their simple, first degree hashes are not unique.
    def issue_canonical_ids_for_unhandled(self):
        hashes = sorted(self.state.hash_to_bnodes.keys())
        for h in hashes: 
            identifier_list = self.state.hash_to_bnodes[h]
            hash_path_list = [] 

            for n in identifier_list: 
                if self.state.canonical_issuer.is_set(n):
                    continue
                temporary_issuer = commons.IDIssuer(prefix = 'b')
                temporary_issuer.issueID(n)
                result = hash_n_degree_quads.compute_n_degree_hash(self.state, n, temporary_issuer)
                hash_path_list.append(result)

            ordered_hash_path_list = sorted(hash_path_list, key=lambda x: x[0])

            for result in ordered_hash_path_list:
                for (existing, _) in result[1]:
                    self.state.canonical_issuer.issueID(existing)



    # Step 6 
    # This function replaces the blank node identifiers in the graph with the canonical 
    # identifiers and returns a new graph with the canonical identifiers.
    def update_graph(self, g: Graph):
        new_g = Graph()
        for s, p, o in g.triples((None, None, None)):
            if isinstance(s, BNode):
                cn_id = self.state.canonical_issuer.map(s.toPython())
                ns = BNode(cn_id)
            else:
                ns = s
            if isinstance(o, BNode):
                cn_id = self.state.canonical_issuer.map(o.toPython())
                no = BNode(cn_id)
            else:
                no = o
            new_g.add((ns, p, no))
        return new_g


    def to_canonical_graph(self, g: Graph):
        self.init_bnode_to_quads(g)
        self.hash_first_degree()
        self.issue_canonical_ids()

        if len(self.state.hash_to_bnodes) > 0:
            logger.info("There are still bnodes with multiple hashes")
            self.issue_canonical_ids_for_unhandled()
        
        cg = self.update_graph(g)

        return cg
        
        
if __name__ == "__main__":
    import sys
    g = Graph()
    g.parse(sys.argv[1], format='nt')
    r = Rdfc10()
    cg = r.to_canonical_graph(g)

    if cg is not None:
        o = cg.serialize(format='nt')
        o = o.split('\n')
        o.sort()
        print('\n'.join(o))
    


        
