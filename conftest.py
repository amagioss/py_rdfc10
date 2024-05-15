import os
import glob

def pytest_configure(config):
    test_input_dirpath  = os.path.join(os.path.dirname(__file__), "tests/test_data")
    # register markers 
    files = glob.glob(test_input_dirpath + "/*-in.nq")
    for file in files:
        tin = file.split("/")[-1] 
        mark = tin.split("/")[-1].split("-")[0]
        config.addinivalue_line("markers", mark + ": refer to tests for description")