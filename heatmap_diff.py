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
            excitatory_cell_labels,
            inhibtory_cell_labels,
            model,
            variant_one,
            variant_two,
            "weight",
            weight_filename,
        )
        heatmap_diff(
            prob_data_one,
            prob_data_two,
            excitatory_cell_labels,
            inhibtory_cell_labels,
            model,
            variant_one,
            variant_two,
            "prob",
            prob_filename,
        )
        return
    if model == "A1":
        # Var One - v29
        # Var Two - v15
        (
            A1_FIELD_NAMES_VAR_ONE,
            A1_LOOKUP_TABLE_VAR_ONE,
            A1_IN_LABELS,
            A1_EX_LABELS,
        ) = generate_a1_data()
        (
            A1_FIELD_NAMES_VAR_TWO,
            A1_LOOKUP_TABLE_VAR_TWO,
            _,
            _,
        ) = generate_a1_data(False)

        weight_data_one, prob_data_one = load_A1_connParams(
            filename_one,
            A1_MAX_ROW,
            A1_MAX_COL,
            sorted(A1_FIELD_NAMES_VAR_ONE),
            A1_LOOKUP_TABLE_VAR_ONE,
        )
        weight_data_two, prob_data_two = load_A1_connParams(
            filename_two,
            A1_MAX_ROW,
            A1_MAX_COL,
            sorted(A1_FIELD_NAMES_VAR_TWO),
            A1_LOOKUP_TABLE_VAR_TWO,
        )
        heatmap_diff(
            weight_data_one,
            weight_data_two,
            A1_EX_LABELS,
            A1_IN_LABELS,
            model,
            variant_one,
            variant_two,
            "weight",
            weight_filename,
        )
        heatmap_diff(
            prob_data_one,
            prob_data_two,
            A1_EX_LABELS,
            A1_IN_LABELS,
            model,
            variant_one,
            variant_two,
            "prob",
            prob_filename,
        )


if __name__ == "__main__":
    main()
