import json
import argparse
from pprint import pprint
from typing import Any, Dict
from os import listdir
from os.path import isfile, join
from deepdiff import DeepDiff

from lib import apply_lsh

CELL_PARAMS = [
    "popParams",
    "cellParams",
    "synMechParams",
    "connParams",
    "stimSourceParams",
    "stimTargetParams",
]


def parse_netpyne_file(data_dict: Dict[str, Any]) -> Dict[str, str]:
    result = {}
    for k in CELL_PARAMS:
        if k not in data_dict:
            print(f"{k} key was not found")
            exit(1)
        if not data_dict[k]:
            value = "{}"
        else:
            value = json.dumps(data_dict[k], sort_keys=True)

        result[k] = value

    return result


def read_netpyne_file(file_path: str):
    netpyne_data = open(file_path, "r")
    netpyne_json = json.load(netpyne_data)
    if "net" not in netpyne_json:
        print(f"{file_path} is missing key 'net'")
        exit(1)
    if "params" not in netpyne_json["net"]:
        print(f"{file_path} is missing key 'params'")
        exit(1)
    return netpyne_json["net"]["params"]


def run():
    parser = argparse.ArgumentParser(prog="NetPyne Tester", description="Test NetPyne")

    parser.add_argument("input")
    parser.add_argument("threshold")
    parser.add_argument("--diff", default=True, action="store_true")

    args = parser.parse_args()

    files = [
        join(args.input, f) for f in listdir(args.input) if isfile(join(args.input, f))
    ]
    file_params = {f: parse_netpyne_file(read_netpyne_file(f)) for f in files}
    result = {}
    data = []
    for param in CELL_PARAMS:
        data = [
            (filename, data_dict[param]) for filename, data_dict in file_params.items()
        ]

        res, pairs = apply_lsh(data, args.threshold)
        result[param] = (res, pairs)

    for params, res in result.items():
        print(f"Results for {params}")
        print(res[0])
        for (
            file1,
            file2,
            score,
        ) in res[1]:
            print(f"{file1} and {file2} have a similarity score of {score}")
            if abs(float(score) - 1.0) > 0.0001:
                f1 = json.loads(file_params[file1][params])
                f2 = json.loads(file_params[file2][params])
                print(f"Data for {file1}")
                pprint(f1, indent=4, width=80, depth=4)
                print()
                print(f"Data for {file2}")
                pprint(f2, indent=4, width=80, depth=4)
                print()
                print(f"Differences for {params}")
                param_diff = DeepDiff(f1, f2, ignore_order=True)
                pprint(param_diff, indent=4, width=80, depth=4)



if __name__ == "__main__":
    run()
