import pytest 
import os
import glob
from os import path
import rdfc10
from rdfc10.rdfc10 import Rdfc10
from rdflib import Graph
from rdflib.compare import to_isomorphic, graph_diff



@pytest.fixture
def test_input_dirpath():
    return os.path.join(os.path.dirname(__file__), "test_data")


def all_tests():
    test_input_dirpath = os.path.join(os.path.dirname(__file__), "test_data")
    pytest_params = []
    files = glob.glob(test_input_dirpath + "/*-in.nq")
    for file in files:
        tin = file.split("/")[-1] 
        tout = file.replace("-in.nq", "-rdfc10.nq")
        mark = tin.split("/")[-1].split("-")[0]
        m = eval(f"pytest.mark.{mark}")
        py_mark = pytest.param(tin, tout, marks=m)
        pytest_params.append(py_mark)
    return pytest_params



@pytest.mark.parametrize(
    "tin, tout", all_tests())
def test_rdfc10(tin, tout, test_input_dirpath):
    g = Graph()
    tpath = path.join(test_input_dirpath, tin)
    g.parse(tpath, format='nt')
    r = Rdfc10()
    cg = r.to_canonical_graph(g)

    serialized_cg = sorted(cg.serialize(format='nt').split('\n'))

    serialized_cg = '\n'.join(serialized_cg).strip()
    with open(path.join(test_input_dirpath, tout)) as f:
        expected = f.read()
        expected = expected.strip()

    if serialized_cg != expected:
        print("\n\n")
        print(serialized_cg)
        print("\n\n")
        print(expected)
        assert  False

    if cg is not None:
        o = cg.serialize(format='nt')
        o = o.split('\n')
        o.sort()


def test_graph_diff(test_input_dirpath):
    g1 = Graph()
    g2 = Graph() 
    g1.parse(path.join(test_input_dirpath, "series.nt"), format='nt')
    g2.parse(path.join(test_input_dirpath, "series.ttl"), format='turtle')
    in_both, in_first, in_second = rdfc10.graph_diff(g1, g2)

    print(len(in_both), len(in_first), len(in_second))

def test_to_hash(test_input_dirpath):
    g1 = Graph()
    g2 = Graph() 
    g1.parse(path.join(test_input_dirpath, "series.nt"), format='nt')
    g2.parse(path.join(test_input_dirpath, "series.ttl"), format='turtle')

    h1 = rdfc10.to_hash(g1)
    h2 = rdfc10.to_hash(g2)

    assert h1 == h2
