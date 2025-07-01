import numpy as np
from numpy.typing import NDArray
import re
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
from enum import Enum


def generate_a1_data() -> tuple[
    list[str], dict[str, {tuple[int, int]}], list[str], list[str]
]:
    field_names = []
    lookup_table = {}
    ex_labels = set([])
    in_labels = []

    row, col = 0, 0
    for in_cell, in_layers in A1_IN_LAYERS.items():
        for in_layer in in_layers:
            col = 0
            in_labels.append(f"{in_cell}{in_layer}")
            for ex_cell, ex_layers in A1_EX_LAYERS.items():
                for ex_layer in ex_layers:
                    ex_labels.add(f"{ex_cell}{ex_layer}")
                    field_name = f"IE_{in_cell}{in_layer}_{ex_cell}{ex_layer}_"
                    field_name = field_name + in_layer[0]
                    field_names.append(field_name)
                    lookup_table[field_name] = (row, col)
                    col += 1
            row += 1
    return field_names, lookup_table, in_labels, list(ex_labels)


M1_CONN_TYPES = set(
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

CONN_TYPES_v101 = set(
    [
        "SOM_IT_",
        "SOM_PT_",
        "SOM_CT_",
        "PV_IT_",
        "PV_PT_",
        "PV_CT_",
        "VIP_IT_",
        "VIP_PT_",
        "VIP_CT_",
        "NGF_IT_",
        "NGF_PT_",
        "NGF_CT_",
    ]
)

M1_INHIBITORY_CELL_NAMES = {"SOM": 0, "PV": 1, "VIP": 2, "NGF": 3}
M1_EXCITATORY_CELL_NAMES = {"IT": 0, "PT": 1, "CT": 2}

M1_MAX_ROW = 12
M1_MAX_COL = 9
M1_OFF_SET = 3

A1_INHIBITORY_CELL_NAMES = {"SOM": 0, "PV": 1, "VIP": 2, "NGF": 3}
A1_LAYER_X0 = set(["2", "3", "4", "5A", "5B", "6"])
A1_LAYER_A0 = set(["1", "2", "3", "4", "5A", "5B", "6"])
A1_IN_LAYERS = {
    "SOM": A1_LAYER_X0,
    "PV": A1_LAYER_X0,
    "VIP": A1_LAYER_X0,
    "NGF": A1_LAYER_A0,
}
A1_EX_LAYER_CT = set(["5A", "5B", "6"])
A1_EX_LAYER_PT = set(["5B"])
A1_EX_LAYER_IT = set(["2", "3", "5A", "5B", "6", "P4", "S4"])
A1_EX_LAYERS = {"CT": A1_EX_LAYER_CT, "PT": A1_EX_LAYER_PT, "IT": A1_EX_LAYER_IT}

A1_MAX_ROW = (
    len(A1_IN_LAYERS["SOM"])
    + len(A1_IN_LAYERS["PV"])
    + len(A1_IN_LAYERS["VIP"])
    + len(A1_IN_LAYERS["NGF"])
)

A1_MAX_COL = len(A1_EX_LAYER_CT) + len(A1_EX_LAYER_PT) + len(A1_EX_LAYER_IT)
A1_OFF_SET = 0

A1_FIELD_NAMES, A1_LOOKUP_TABLE, A1_IN_LABELS, A1_EX_LABELS = generate_a1_data()


class CellType(Enum):
    INHIBITORY = 1
    EXCITATORY = 2


def generate_label_m1(cell_type: CellType) -> list[str]:
    labels = []
    cells = None
    if cell_type == CellType.INHIBITORY:
        cells = M1_INHIBITORY_CELL_NAMES
    else:
        cells = M1_EXCITATORY_CELL_NAMES

    for cell in cells.keys():
        for i in range(3):
            label = f"{cell} layer {i}"
            labels.append(label)
    return labels


def load_M1_connParams(file_path, max_row, max_col: str) -> NDArray[np.float64]:
    data = np.zeros((max_row, max_col))
    conn_params = pd.read_json(file_path)

    conn = {}

    for conn_type in CONN_TYPES_v101:
        for key, value in conn_params.items():
            if conn_type in key:
                conn[key] = value.to_dict()

    for key, value in conn.items():
        cells = key.split("_")
        in_cell = cells[1]
        ex_cell = cells[2]
        ex_layers = re.findall("\d+", ex_cell)
        in_layers = re.findall("\d+", in_cell)
        in_index = (M1_OFF_SET * M1_INHIBITORY_CELL_NAMES[in_cell]) + int(ex_layers[0])
        ex_index = (M1_OFF_SET * M1_EXCITATORY_CELL_NAMES[ex_cell]) + int(in_layers[1])
        data[in_index][ex_index] = value["weight"]

    return data


def load_A1_connParams(
    file_path: str, max_row: int, max_col: int
) -> NDArray[np.float64]:
    data = np.zeros((max_row, max_col))
    conn_params = pd.read_json(file_path)

    for conn_type in A1_FIELD_NAMES:
        for key, value in conn_params.items():
            if conn_type == key:
                weight = value.to_dict()["weight"]
                (row, col) = A1_LOOKUP_TABLE[key]
                data[row][col] = weight

    return data


def main():
    # inhibtory_cell_labels = generate_label_m1(CellType.INHIBITORY)
    # excitatory_cell_labels = generate_label_m1(CellType.EXCITATORY)
    # data = load_connParams("./m1/v101_connParams.json", M1_MAX_ROW, M1_MAX_COL)
    # graph = sns.heatmap(
    #     data,
    #     cmap="YlGnBu",
    #     xticklabels=excitatory_cell_labels,
    #     yticklabels=inhibtory_cell_labels,
    # )
    # graph.set_title("M1 v101 Conn Params")
    # graph.xaxis.tick_top()
    # graph.xaxis.set_label_position("top")
    #
    # plt.show()

    print(A1_IN_LABELS)
    print(len(A1_IN_LABELS))

    data = load_A1_connParams(
        "./a1/a1-netparams_conn_params.json", A1_MAX_ROW, A1_MAX_COL
    )
    graph = sns.heatmap(
        data, cmap="YlGnBu"
        , xticklabels=A1_EX_LABELS, 
        yticklabels=A1_IN_LABELS
    )
    graph.set_title("A1 Conn Params")
    graph.xaxis.tick_top()
    graph.xaxis.set_label_position("top")

    plt.show()


if __name__ == "__main__":
    main()
