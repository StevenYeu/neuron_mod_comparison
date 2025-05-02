import numpy as np
from numpy.typing import NDArray
import re
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt

CONN_TYPE = "SOM_PT_HH_full"


def load_connParams(file_path: str) -> NDArray[np.float64]:
    conn_params = pd.read_json(file_path)
    som_pt = {key: value.to_dict() for key, value in conn_params.items() if CONN_TYPE in key}

    som_max_layer = 0
    pt_max_layer = 0

    for key in som_pt.keys():
        layers = re.findall("\d+", key)
        if len(layers) > 2:
            print(f"Found {len(layers)} layers")
        som_max_layer = max(som_max_layer, int(layers[0]))
        pt_max_layer = max(pt_max_layer, int(layers[1]))

    print(f"Max SOM layer is {som_max_layer + 1}")
    print(f"Max PT layer is {pt_max_layer + 1}")

    data = np.zeros((som_max_layer + 1, pt_max_layer + 1))

    for key, value in som_pt.items():
        layers = re.findall("\d+", key)
        print(value)
        som_layer = int(layers[0])
        pt_layer = int(layers[1])
        if len(layers) > 2:
            print(f"Found {len(layers)} layers")
        data[som_layer][pt_layer] = value["weight"]

    print(data)

    return data


def main():
    data = load_connParams("./m1/v103_connParams.json")
    sns.heatmap(data, cmap="YlGnBu")

    plt.title("SOM to PT")
    plt.savefig('m1_v103_som_pt.png')
    # plt.show()


if __name__ == "__main__":
    main()
