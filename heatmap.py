import matplotlib.pylab as plt
import argparse

from util import heatmap
from util.heatmap import heatmap as hmap


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
    hmap(filename, model, variant)


if __name__ == "__main__":
    main()
