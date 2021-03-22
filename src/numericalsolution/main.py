import sys
import math

from src.numericalsolution.math import derivative
from src.numericalsolution.response import Response
from src.numericalsolution.validation import validate_input


def solve(f, lo, hi, eps_x, eps_y, method, settings={}):
    err = validate_input(f, lo, hi, eps_x, eps_y)
    if err is not None:
        return generate_bad_response(err)

    methods = {
        'bisections': bisections,
        'chords': chords,
        'newton': newton,
    }

    return methods[method](f, lo, hi, eps_x, eps_y, settings)


MAX_ITERATION = 100


def bisections(f, lo, hi, eps_x, eps_y, settings):
    curr_a = lo
    curr_b = hi
    i = 0

    prev_x = sys.float_info.min
    prev_y = sys.float_info.min

    while True:
        i += 1

        curr_x = (curr_a + curr_b) / 2
        curr_y = f(curr_x)

        lim = check_limits(lo, hi, curr_x, prev_x, eps_x, i)
        if lim is not None:
            return lim

        lim = check_limits_y(curr_y, prev_y, eps_y, curr_x)
        if lim is not None:
            return lim

        prev_x = curr_x
        prev_y = curr_y

        if f(curr_a) * curr_y < 0:
            curr_a = curr_a
            curr_b = curr_x
        elif f(curr_b) * curr_y < 0:
            curr_a = curr_x
            curr_b = curr_b
        elif curr_y == 0:
            return generate_response(True, curr_x, "Found exact solution.")
        else:
            return generate_bad_response("Fail")


def chords(f, lo, hi, eps_x, eps_y, settings):
    curr_x, prev_x, i = lo, lo + 2 * eps_x, 0

    while True:
        lim = check_limits(lo, hi, curr_x, prev_x, eps_x, i)
        if lim is not None:
            return lim

        curr_x = curr_x - f(curr_x) / (f(curr_x) - f(prev_x)) * (curr_x - prev_x)
        prev_x = curr_x
        i += 1


def newton(f, lo, hi, eps_x, eps_y, settings):
    curr_x, prev_x, i = lo, lo + 2 * eps_x, 0
    while True:
        lim = check_limits(lo, hi, curr_x, prev_x, eps_x, i)
        if lim is not None:
            return lim

        der = derivative(f, curr_x)
        # if der == 0:
        #     return None

        prev_x = curr_x
        curr_x = curr_x - f(curr_x) / der
        i += 1


def check_limits(lo, hi, curr_x, prev_x, eps_x, i=-1):
    if abs(prev_x - curr_x) < eps_x:
        return generate_response(True, curr_x, "Epsilon X break.")

    if curr_x > hi:
        return generate_response(True, curr_x, "X ran out of Hi.")

    if curr_x < lo:
        return generate_response(True, curr_x, "X ran out of Low.")


def check_limits_y(curr_y, prev_y, eps_y, curr_x):
    if abs(prev_y - curr_y) < eps_y:
        return generate_response(True, curr_x, "Epsilon Y break.")


def generate_bad_response(message):
    return Response(False, sys.float_info.max, message);


def generate_response(is_ok, x, message=""):
    return Response(is_ok, x, message);
