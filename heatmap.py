import matplotlib.pylab as plt
import argparse

from util.heatmap import (
    generate_a1_data,
    load_A1_connParams,
    generate_label_m1,
    load_M1_connParams,
    M1_MAX_COL,
    M1_MAX_ROW,
    CellType,
    save_graph,
    A1_MAX_ROW,
    A1_MAX_COL,
)


def main():
    parser = argparse.ArgumentParser(
        prog="HeatMap Generator",
        description="Generate Heat for NetPyne Data",
    )
    parser.add_argument("filename")
    parser.add_argument("model")
    parser.add_argument("variant")
    args = parser.parse_args()
    model = args.model
    filename = args.filename
    variant = args.variant
    weight_graph_name = (f"{model} {variant} Conn Params - Weight",)
    prob_graph_name = (f"{model} {variant} Conn Params - Probability",)
    filename_split = filename.split(".")
    weight_filename = f"{filename_split[0]}_weight.png"
    prob_filename = f"{filename_split[0]}_prob.png"
    if model == "M1":
        inhibtory_cell_labels = generate_label_m1(CellType.INHIBITORY)
        excitatory_cell_labels = generate_label_m1(CellType.EXCITATORY)
        weight_data, prob_data = load_M1_connParams(
            filename, M1_MAX_ROW, M1_MAX_COL, variant
        )
        save_graph(
            weight_graph_name,
            weight_data,
            excitatory_cell_labels,
            inhibtory_cell_labels,
            weight_filename,
        )

        save_graph(
            prob_graph_name,
            prob_data,
            excitatory_cell_labels,
            inhibtory_cell_labels,
            prob_filename,
        )
        return
    if model == "A1":
        A1_FIELD_NAMES, A1_LOOKUP_TABLE, A1_IN_LABELS, A1_EX_LABELS = generate_a1_data()
        if variant == "v15":
            A1_FIELD_NAMES, A1_LOOKUP_TABLE, A1_IN_LABELS, A1_EX_LABELS = (
                generate_a1_data(False)
            )

        weight_data, prob_data = load_A1_connParams(
            filename,
            A1_MAX_ROW,
            A1_MAX_COL,
            A1_FIELD_NAMES,
            A1_LOOKUP_TABLE,
        )
        save_graph(weight_graph_name, weight_data, A1_EX_LABELS, A1_IN_LABELS)
        save_graph(prob_graph_name, prob_data, A1_EX_LABELS, A1_IN_LABELS)

    plt.show()


if __name__ == "__main__":
    main()
