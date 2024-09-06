import argparse
import json
import sys

import matplotlib
from matplotlib import pyplot as plt

matplotlib.use("Agg")


def create_parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--path_to_results", nargs="?", default="./result")

    return argument_parser


def create_accuracy_graph(path_to_results: str):
    figure = plt.figure(figsize=(12, 5))

    sub_plot_accuracy = figure.add_subplot(1, 2, 1)
    plt.xlabel("Step number", fontsize="xx-large")
    plt.ylabel("Accuracy", fontsize="xx-large")

    for strategy in ["Micro", "Macro", "Meso"]:
        x_value = []
        for i in [1, 2, 3, 4, 5, 6]:
            with open(path_to_results + f"/{i}/" + strategy + "/result.json", "r") as file:
                result = json.load(file)
                i_value = [value for value in result["accuracy"]]
                if len(x_value) == 0:
                    x_value = i_value.copy()
                else:
                    for j, i_value in zip(range(len(i_value)), i_value):
                        x_value[j] += i_value

        for i in range(len(x_value)):
            x_value[i] /= 6

        plt.plot(range(len(x_value)), x_value, label=strategy)
    plt.legend(loc="upper right")

    sub_plot_diameter = figure.add_subplot(1, 2, 2)
    plt.xlabel("Step number", fontsize="xx-large")
    plt.ylabel("Diameter", fontsize="xx-large")

    for strategy in ["Micro", "Macro", "Meso"]:
        x_value = []
        for i in [1, 2, 3, 4, 5, 6]:
            with open(path_to_results + f"/{i}/" + strategy + "/result.json", "r") as file:
                result = json.load(file)
                i_value = [value for value in result["diameter"]]
                if len(x_value) == 0:
                    x_value = i_value.copy()
                else:
                    for j, i_value in zip(range(len(i_value)), i_value):
                        x_value[j] += i_value

        for i in range(len(x_value)):
            x_value[i] /= 6

        plt.plot(range(len(x_value)), x_value, label=strategy)
    plt.legend(loc="upper right")

    plt.savefig(path_to_results + f"/merged_accuracy.svg", transparent=False, facecolor="white", dpi=300)


def main():
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    print(args)

    create_accuracy_graph(path_to_results=args.path_to_results)


if __name__ == "__main__":
    main()
