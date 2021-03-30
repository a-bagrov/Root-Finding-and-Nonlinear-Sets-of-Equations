#!/usr/bin/env python3
import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

from src.numericalsolution.numerical_solver import NumericalSolver, methods


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
    # parser.add_argument("output", help="Path to output file to print results. File will be overwritten.", type=str)
    parser.add_argument("-m", "--methods", help="Methods that be used in solving, for example 'bisections,chords'. "
                                                "No space between methods.", type=str)
    parser.add_argument("-eps_x", "--epsilon_x", help="Accuracy by x axis.", type=float, default=1e-7)
    parser.add_argument("-eps_y", "--epsilon_y", help="Accuracy by y axis.", type=float, default=1e-7)

    args = parser.parse_args()
    inputp = args.input
    # output = args.output
    check_path(inputp, True)
    # check_path(output)

    if args.methods is None:
        args.methods = methods

    res_dic = dict()
    call_number_by_method = dict()
    iters_by_method = dict()
    for method in args.methods:
        res_dic[method] = list()
        call_number_by_method[method] = list()
        iters_by_method[method] = list()

    res = NumericalSolver.solve_from_file_data(inputp, args.epsilon_x, args.epsilon_y, args.methods)
    for i in res:
        for j in i.values():
            res_dic[j.method].append(j)

    total_eqs = len(res_dic[args.methods[0]])
    print(f"Processed {total_eqs} equations.")

    for method in args.methods:
        good = 0
        bad = 0
        calls_number = 0
        iters = 0
        for eqs in res_dic[method]:
            if eqs.is_ok is not True:
                bad += 1
                continue
            else:
                good += 1
                calls_number += eqs.statistics.callsNumbers
                iters += eqs.statistics.iterations

        print(
            f"METHOD {method}. Failed: {bad / total_eqs * 100}% | Avg func calls: {calls_number / good} | Avg iters: {iters / good}")

    for method in res_dic.values():
        for m in method:
            if m.is_ok is True:
                call_number_by_method[m.method].append(m.statistics.callsNumbers)
                iters_by_method[m.method].append(m.statistics.iterations)

    fig, axes = plt.subplots(len(args.methods), 2)
    fig.set_size_inches(18.5, 10.5)
    i = 0

    for method in args.methods:
        axes[i, 0].hist(call_number_by_method[method],
                        bins=np.arange(0, max(call_number_by_method[method]), max(call_number_by_method[method]) / 25))
        axes[i, 0].set(xlabel='Function calls')
        axes[i, 0].set_title(method)
        i += 1

    i = 0
    for method in args.methods:
        axes[i, 1].hist(iters_by_method[method],
                        bins=np.arange(0, max(iters_by_method[method]), max(iters_by_method[method]) / 25))
        axes[i, 1].set(xlabel='Iterations')
        axes[i, 1].set_title(method)
        i += 1

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
