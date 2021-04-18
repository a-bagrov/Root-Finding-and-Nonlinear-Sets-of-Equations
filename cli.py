#!/usr/bin/env python3
import argparse
import concurrent
import os
from os import listdir

import matplotlib.pyplot as plt
import numpy as np

from src.numericalsolution.numerical_solver import NumericalSolver, methods, bisections, chords, newton, brenth


def check_path(path: str, file_need_to_exist: bool = False):
    if file_need_to_exist and os.path.exists(path):
        return

    if os.path.dirname(path) == "":
        return

    if os.path.exists(os.path.dirname(path)):
        return

    raise ValueError(f"Bad path {path}")


def main():
    parser = argparse.ArgumentParser(description="This program is designed to solve equations in numerical way and "
                                                 "print result.")
    parser.add_argument('input', help="Path to file with data.", type=str)
    parser.add_argument("-m", "--methods", help="Methods that be used in solving, for example 'bisections,chords'. "
                                                "No space between methods.", type=str)
    parser.add_argument("-eps_x", "--epsilon_x", help="Accuracy by x axis.", type=float, default=1e-7)
    parser.add_argument("-eps_y", "--epsilon_y", help="Accuracy by y axis.", type=float, default=1e-7)

    args = parser.parse_args()
    inputp = args.input

    if args.methods is None:
        args.methods = [bisections, chords, newton, brenth]

    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        future_to_url = {executor.submit(process_file, file, args, inputp): file for
                         file in listdir(inputp) if file.endswith(".data")}


def process_file(file, args, inputp):
    all_results_by_method = dict()
    call_number_by_method = dict()
    iters_by_method = dict()
    fails_by_method = dict()

    for method in args.methods:
        all_results_by_method[method] = list()
        call_number_by_method[method] = list()
        iters_by_method[method] = list()
        fails_by_method[method] = list()

    res = NumericalSolver.solve_from_file_data(os.path.join(inputp, file), args.epsilon_x, args.epsilon_y,
                                               args.methods)
    for i in res:
        for j in i.values():
            all_results_by_method[j.method].append(j)

    total_eqs = len(all_results_by_method[args.methods[0]])

    methods_output = list()
    methods_output.append(f"Processed {total_eqs} equations.")

    for method in args.methods:
        good = 0
        bad = 0
        calls_number = 0
        iters = 0
        for eqs in all_results_by_method[method]:
            if eqs.is_ok is not True:
                bad += 1
                continue
            else:
                good += 1
                calls_number += eqs.statistics.callsNumbers
                iters += eqs.statistics.iterations

        methods_output.append(
            f"METHOD {method}. Failed: {bad / total_eqs * 100}% | Avg func calls: {calls_number / good} | Avg iters: {iters / good}")

    with open(os.path.join(inputp, f"{file}_REPORT.txt"), "w") as f:
        f.write('\n'.join(methods_output))

    for method in all_results_by_method.values():
        for m in method:
            if m.is_ok is True:
                call_number_by_method[m.method].append(m.statistics.callsNumbers)
                iters_by_method[m.method].append(m.statistics.iterations)

    fig, axes = plt.subplots(len(args.methods), 2)
    fig.set_size_inches(18.5, 10.5)

    i = 0

    max_calls = max(call_number_by_method["bisections"])
    max_iteration = max(iters_by_method["bisections"])

    for method in args.methods:
        axes[i, 1].hist(call_number_by_method[method],
                        density=True,
                        bins=np.arange(0, max_calls, max_calls / 50),
                        color="black")
        axes[i, 1].set(xlabel='Function calls', ylabel="Probability")
        axes[i, 1].set_title(method)
        i += 1

    i = 0

    for method in args.methods:
        axes[i, 0].hist(iters_by_method[method],
                        density=True,
                        bins=np.arange(0, max_iteration, max_iteration / 50),
                        color="black")
        axes[i, 0].set(xlabel='Iterations', ylabel="Probability")
        axes[i, 0].set_title(method)
        i += 1

    plt.tight_layout()
    fig.savefig(os.path.join(inputp, f'{file}_GRAPH.png'), dpi=fig.dpi)


if __name__ == "__main__":
    main()
