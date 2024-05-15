
# RDF Canonicalization in Python

This is an implementation of the [RDF Dataset Canonicalization](https://www.w3.org/TR/rdf-canon/) algorithm, also referred to as RDFC-1.0. The algorithm has been published by the W3C [RDF Dataset Canonicalization and Hash Working Group](https://www.w3.org/groups/wg/rch).

The implementation here is based on typescript implementation present in the following repository:

- https://github.com/iherman/rdfjs-c14n 

Also implements

- graph_diff: Same as in https://rdflib.readthedocs.io/en/stable/_modules/rdflib/compare.html but using the RDFC10 canonicalization algorithm.
- to_hash: Generates a hash after canonicalizing the RDF graph.


## Installation

```bash
pip install .
```

## Running tests

All test cases are in `tests` directory. To run tests, use the following command:

```bash

# Run tests on installed package
pytest --import-mode=importlib -v -s ./tests/test_rdfc10.py 

# Graph diff test 
pytest  --import-mode=importlib -v -s ./tests/test_rdfc10.py -k test_graph_diff

# Hash test
pytest -v -s ./tests/test_rdfc10.py -k test_to_hash

```

## Limitations

- Currently only supporting n-triples. n-quads support is not yet implemented.

