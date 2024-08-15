import json
import argparse
from typing import Any, Dict
from os import listdir
from os.path import isfile, join

from lib import apply_lsh

CELL_PARAMS = ['popParams', 'cellParams', 'synMechParams', "connParams", "stimSourceParams", "stimTargetParams"]

def parse_netpynne_file(data_dict: Dict[str,Any]) -> Dict[str,str]:
    result = {}
    for k in CELL_PARAMS:
        value = json.dumps(data_dict[k],sort_keys=True)
        result[k] = value 

    return result

def read_netpynne_file(file_path: str):
    netpynne_data = open(file_path,'r')
    if 'net' not in netpynne_data:
        print(f"{file_path} is missing key 'net'")
        exit(1)
    return json.load(netpynne_data)['net']['params']


def run():
    parser = argparse.ArgumentParser(prog="LSH Tester", description="Test LSH")

    parser.add_argument("input")
    parser.add_argument("threshold")

    args = parser.parse_args()

    files = [
        join(args.input, f) for f in listdir(args.input) if isfile(join(args.input, f))
    ]
    file_params = { f: parse_netpynne_file(read_netpynne_file(f)) for f in files}

    result = {}

    for param in CELL_PARAMS:
        data = [(filename,data_dict[param]) for filename, data_dict in file_params]
        res, pairs = apply_lsh(data, args.threshold)
        result[param] = (res,pairs)
    

    


if __name__ == "__main__":
   run() 
