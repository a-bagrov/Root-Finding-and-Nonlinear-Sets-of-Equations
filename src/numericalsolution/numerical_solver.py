import concurrent.futures
import sys
from ast import literal_eval as make_tuple

import numpy as np
import scipy
from scipy import optimize

from src.numericalsolution.Common import math
from src.numericalsolution.Common.math import derivative
from src.numericalsolution.DataWrapper.data_wrapper import DataWrapper
from src.numericalsolution.DataWrapper.statistics import Statistics
from src.numericalsolution.DataWrapper.tuple_array_wrapper import TupleArrayWrapper
from src.numericalsolution.response import Response
from src.numericalsolution.validation import validate_input

MAX_ITERATION = 2000
bisections = "bisections"
chords = "chords"
newton = "newton"
brenth = "brenth"
brentq = "brentq"
ridder = "ridder"

methods = [bisections, chords, newton, brenth, brentq]


def parse_line(tuples_str, eps_x, eps_y, methods_to_use):
    tuples_str = tuples_str[2:-1]
    tuple_list = list()
    for tuple_str in tuples_str.split('),'):
        if len(tuple_str) > 1:
            try:
                tuple_list.append(make_tuple(tuple_str + ')'))
            except Exception as e:
                print(e)

    return NumericalSolver.solve_taw_with_methods(TupleArrayWrapper(tuple_list), eps_x, eps_y, methods_to_use)


class NumericalSolver:

    @staticmethod
    def __get_methods():
        return {
            bisections: NumericalSolver.__bisections,
            chords: NumericalSolver.__chords,
            newton: NumericalSolver.__newton,
            brenth: NumericalSolver.__brenth,
            brentq: NumericalSolver.__brentq,
            ridder: NumericalSolver.__ridder
        }

    @staticmethod
    def solve_from_file_data(filepath: str, eps_x: float, eps_y: float, methods_to_use: [] = None):
        if methods_to_use is None:
            methods_to_use = methods

        inf = open(filepath, "r")
        lines = inf.readlines()
        resp_list = list()

        with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
            future_to_url = {executor.submit(parse_line, line, eps_x, eps_y, methods_to_use): line for
                             line in lines if line.startswith("F[(")}
            for future in concurrent.futures.as_completed(future_to_url):
                resp_list.append(future.result())

        return resp_list


    @staticmethod
    def solve_taw_with_methods(taw: TupleArrayWrapper, eps_x: float, eps_y: float, methods_to_use: []):
        hi = taw.get_max_x()
        lo = taw.get_min_x()
        resp = NumericalSolver.solve_with_methods(taw, lo, hi, methods_to_use, eps_x, eps_y)
        return resp

    @staticmethod
    def solve_with_methods(data: DataWrapper, lo: float, hi: float, methods_to_use: [] = None, eps_x: float = 1e-10,
                           eps_y: float = 1e-10, settings: {} = None):
        if methods_to_use is None:
            methods_to_use = methods

        dic = dict()
        for method in methods_to_use:
            dic[method] = NumericalSolver.solve(data, method, lo, hi, eps_x, eps_y, settings)

        return dic

    @staticmethod
    def solve(data: DataWrapper, method: str, lo: float, hi: float, eps_x: float = 1e-10, eps_y: float = 1e-10,
              settings: {} = None):
        """
        Solves the given equation in numerical way.
        @param data: DataWrapper instance.
        @param lo: Start of interval where you expect root.
        @param hi: End of interval where you expect root.
        @param eps_x: Precision by x-axis. If move in root occurred with new iteration is less than eps_x, iteration will break.
        @param eps_y: Precision by y-axis. If move in y occurred with new iteration is less than eps_y, iteration will break.
        @param method: Method to solve equation: 'bisections', 'chord', 'newton', 'brenth', 'brentq', 'rider'.
        @param settings: Construct in progress, ignore.
        @return: Response object
        """
        if settings is None:
            settings = {}
        if not isinstance(data, DataWrapper):
            return NumericalSolver.__generate_bad_response(method, "Bad data parameter.")

        err = validate_input(data, lo, hi, eps_x, eps_y)
        if err is not None:
            return NumericalSolver.__generate_bad_response(method, err)

        if "DELTA_X_DERIVATE" not in settings:
            settings["DELTA_X_DERIVATE"] = math.DELTA_X_DERIVATE

        data.clear_statistics()
        return NumericalSolver.__get_methods()[method](data, method, lo, hi, eps_x, eps_y, settings)

    @staticmethod
    def __bisections(data, method_name, lo, hi, eps_x, eps_y, settings):
        curr_a = lo
        curr_b = hi
        i = 0

        prev_x = sys.float_info.min
        prev_y = sys.float_info.min

        while True:
            i += 1

            curr_x = (curr_a + curr_b) / 2
            curr_y = data.get_value_at(curr_x)

            lim = NumericalSolver.__check_limits(data, method_name, lo, hi, curr_x, prev_x, eps_x, i)
            if lim is not None:
                return lim

            lim = NumericalSolver.__check_limits_y(data, method_name, curr_y, prev_y, eps_y, curr_x, i)
            if lim is not None:
                return lim

            prev_x = curr_x
            prev_y = curr_y

            if data.get_value_at(curr_a) * curr_y < 0:
                curr_a = curr_a
                curr_b = curr_x
            elif data.get_value_at(curr_b) * curr_y < 0:
                curr_a = curr_x
                curr_b = curr_b
            elif curr_y == 0:
                return NumericalSolver.__generate_response(data, True, i, method_name, curr_x,
                                                           "Found exact solution.")
            else:
                return NumericalSolver.__generate_bad_response(method_name, "Fail")

    @staticmethod
    def __chords(data, method_name, lo, hi, eps_x, eps_y, settings):
        curr_x = lo
        prev_x = lo + 2e-5 if eps_x < 2e-5 else lo + 2 * eps_x
        i = 0

        while True:
            lim = NumericalSolver.__check_limits(data, method_name, lo, hi, curr_x, prev_x, eps_x, i)
            if lim is not None:
                return lim

            curr_x, prev_x = curr_x - data.get_value_at(curr_x) / (
                    data.get_value_at(curr_x) - data.get_value_at(prev_x)) * (curr_x - prev_x), curr_x
            i += 1

    @staticmethod
    def __newton(data, method_name, lo, hi, eps_x, eps_y, settings):
        curr_x = lo
        prev_x = lo + 2e-5 if eps_x < 2e-5 else lo + 2 * eps_x
        i = 0

        while True:
            lim = NumericalSolver.__check_limits(data, method_name, lo, hi, curr_x, prev_x, eps_x, i)
            if lim is not None:
                return lim

            der = derivative(data, curr_x, settings["DELTA_X_DERIVATE"])
            # if der == 0:
            #     return None

            prev_x = curr_x
            curr_x = curr_x - data.get_value_at(curr_x) / der
            i += 1

    @staticmethod
    def __brenth(data, method_name, lo, hi, eps_x, eps_y, settings):
        xtol = eps_x
        rtol = eps_y if eps_y > 8.88178e-16 else 4 * np.finfo(float).eps

        ans = scipy.optimize.brenth(data, lo, hi, (), xtol, rtol, MAX_ITERATION, True, False)
        return NumericalSolver.__generate_response(data, ans[1].converged, ans[1].iterations, method_name, ans[0],
                                                   ans[1].flag)

    @staticmethod
    def __ridder(data, method_name, lo, hi, eps_x, eps_y, settings):
        xtol = eps_x
        rtol = eps_y if eps_y > 8.88178e-16 else 4 * np.finfo(float).eps

        ans = scipy.optimize.ridder(data, lo, hi, (), xtol, rtol, MAX_ITERATION, True, False)
        return NumericalSolver.__generate_response(data, ans[1].converged, ans[1].iterations, method_name, ans[0],
                                                   ans[1].flag)

    @staticmethod
    def __brentq(data, method_name, lo, hi, eps_x, eps_y, settings):
        xtol = eps_x
        rtol = 4 * np.finfo(float).eps

        ans = scipy.optimize.brentq(data, lo, hi, (), xtol, rtol, MAX_ITERATION, True, False)
        return NumericalSolver.__generate_response(data, ans[1].converged, ans[1].iterations, method_name, ans[0],
                                                   ans[1].flag)

    @staticmethod
    def __check_limits(data, method_name, lo, hi, curr_x, prev_x, eps_x, iterations):
        if abs(prev_x - curr_x) < eps_x:
            return NumericalSolver.__generate_response(data, True, iterations, method_name, curr_x,
                                                       "Epsilon X break.")

        if curr_x > hi:
            return NumericalSolver.__generate_response(data, True, iterations, method_name, curr_x,
                                                       "X ran out of Hi.")

        if curr_x < lo:
            return NumericalSolver.__generate_response(data, True, iterations, method_name, curr_x,
                                                       "X ran out of Low.")

    @staticmethod
    def __check_limits_y(data: DataWrapper, method_name: str, curr_y: float, prev_y: float, eps_y: float,
                         curr_x: float, iterations: int):
        if abs(prev_y - curr_y) < eps_y:
            return NumericalSolver.__generate_response(data, True, iterations, method_name, curr_x,
                                                       "Epsilon Y break.")

    @staticmethod
    def __generate_bad_response(method_name: str, message: str):
        return Response(False, sys.float_info.min, method_name, message, None)

    @staticmethod
    def __generate_response(data: DataWrapper, is_ok: bool, iterations: int, method_name: str, x: float,
                            message: str = ""):
        stat = data.get_statistics()
        return Response(is_ok, x, method_name, message, Statistics(stat, iterations))
