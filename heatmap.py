import numpy as np
from numpy.typing import NDArray
import re
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
from enum import Enum

CONN_TYPES = set(
    [
        "SOM_IT_HH_full",
        "SOM_PT_HH_full",
        "SOM_CT_HH_full",
        "PV_IT_HH_full",
        "PV_PT_HH_full",
        "PV_CT_HH_full",
        "VIP_IT_HH_full",
        "VIP_PT_HH_full",
        "VIP_CT_HH_full",
        "NGF_IT_HH_full",
        "NGF_PT_HH_full",
        "NGF_CT_HH_full",
    ]
)

INHIBITORY_CELL = {"SOM": 0, "PV": 1, "VIP": 2, "NGF": 3}
EXCITATORY_CELL = {"IT": 0, "PT": 1, "CT": 2}

MAX_ROW = 12
MAX_COL = 9
OFF_SET = 3


class CellType(Enum):
    INHIBITORY = 1
    EXCITATORY = 2


def generate_label(cell_type: CellType) -> list[str]:
    labels = []
    cells = None
    if cell_type == CellType.INHIBITORY:
        cells = INHIBITORY_CELL
    else:
        cells = EXCITATORY_CELL

    for cell in cells.keys():
        for i in range(3):
            label = f"{cell} layer {i}"
            labels.append(label)
    return labels


def load_connParams(file_path: str) -> NDArray[np.float64]:
    data = np.zeros((MAX_ROW, MAX_COL))
    conn_params = pd.read_json(file_path)

    conn = {}

    for conn_type in CONN_TYPES:
        for key, value in conn_params.items():
            if conn_type in key:
                conn[key] = value.to_dict()

    for key, value in conn.items():
        cells = key.split("_")
        in_cell = cells[0]
        ex_cell = cells[1]
        layers = re.findall("\d+", key)
        in_index = (OFF_SET * INHIBITORY_CELL[in_cell]) + int(layers[0])
        ex_index = (OFF_SET * EXCITATORY_CELL[ex_cell]) + int(layers[1])
        data[in_index][ex_index] = value["weight"]

    return data


def main():
    inhibtory_cell_labels = generate_label(CellType.INHIBITORY)
    excitatory_cell_labels = generate_label(CellType.EXCITATORY)
    data = load_connParams("./m1/v103_connParams.json")
    graph = sns.heatmap(
        data,
        cmap="YlGnBu",
        xticklabels=excitatory_cell_labels,
        yticklabels=inhibtory_cell_labels,
    )
    graph.set_title("M1 v103 Conn Params")
    graph.xaxis.tick_top()
    graph.xaxis.set_label_position("top")

    # plt.xlabel("Excitatory Cells")
    # plt.ylabel("Inhibitory Cells")

    plt.show()


if __name__ == "__main__":
    main()
