import argparse
from util.heatmap import (
    generate_a1_data,
    heatmap_diff,
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
        prog="HeatMap Difference",
        description="Generate Heatmap Difference for NetPyne Data",
    )
    parser.add_argument("filename_one")
    parser.add_argument("filename_two")
    parser.add_argument("variant_one")
    parser.add_argument("variant_two")
    parser.add_argument("model")
    args = parser.parse_args()
    model = args.model
    filename_one = args.filename_one
    filename_two = args.filename_two
    variant_one = args.variant_one
    variant_two = args.variant_two
    weight_graph_name = (
        f"{model} {variant_one} and {variant_two} Difference Conn Params - Weight",
    )
    prob_graph_name = (
        f"{model} {variant_one} and {variant_two} Difference Conn Params - Probability",
    )
    weight_filename = f"{model}_diff_{variant_one}_{variant_two}_weight.png"
    prob_filename = f"{model}_diff_{variant_one}_{variant_two}_prob.png"
    if model == "M1":
        inhibtory_cell_labels = generate_label_m1(CellType.INHIBITORY)
        excitatory_cell_labels = generate_label_m1(CellType.EXCITATORY)
        weight_data_one, prob_data_one = load_M1_connParams(
            filename_one, M1_MAX_ROW, M1_MAX_COL, variant_one
        )
        weight_data_two, prob_data_two = load_M1_connParams(
            filename_two, M1_MAX_ROW, M1_MAX_COL, variant_two
        )
        heatmap_diff(
            weight_data_one,
            weight_data_two,
            inhibtory_cell_labels,
            excitatory_cell_labels,
            model,
            variant_one,
            variant_two,
            "weight",
            weight_filename
        )
        heatmap_diff(
            prob_data_one,
            prob_data_two,
            inhibtory_cell_labels,
            excitatory_cell_labels,
            model,
            variant_one,
            variant_two,
            "prob",
            prob_filename
        )
        return
    if model == "A1":
        A1_FIELD_NAMES, A1_LOOKUP_TABLE, A1_IN_LABELS, A1_EX_LABELS = generate_a1_data()
        if variant_one == "v15":
            A1_FIELD_NAMES, A1_LOOKUP_TABLE, A1_IN_LABELS, A1_EX_LABELS = (
                generate_a1_data(False)
            )

        weight_data, prob_data = load_A1_connParams(
            filename_one,
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
