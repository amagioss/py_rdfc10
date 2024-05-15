

from .rdfc10 import Rdfc10
from .commons import compute_hash
from rdflib import Graph
from typing import Tuple

def graph_diff(g1: Graph, g2: Graph) -> Tuple[Graph, Graph, Graph]:
    """Returns three sets of triples: "in both", "in first" and "in second"."""
    # bnodes have deterministic values in canonical graphs:
    cg1 = Rdfc10().to_canonical_graph(g1)
    cg2 = Rdfc10().to_canonical_graph(g2)
    in_both = cg1 * cg2
    in_first = cg1 - cg2
    in_second = cg2 - cg1
    return (in_both, in_first, in_second)


def to_hash(g: Graph) -> str:
    """Returns a graph with blank nodes replaced by their hashes."""
    g = Rdfc10().to_canonical_graph(g)
    all_triples_n3 = [f"{t[0].n3()} {t[1].n3()} {t[2].n3()} ." for t in g]
    all_triples_n3 = sorted(all_triples_n3)

    all_triples_str = "\n".join(all_triples_n3)
    hash_val = compute_hash('sha256', all_triples_str)
    print(f"Hash of the graph: {hash_val}")
    return hash_val