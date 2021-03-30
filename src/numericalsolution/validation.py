def validate_input(f, a, b, eps_x, eps_y):
    if b < a:
        return "Wrong interval"

    if f.get_value_at(a) * f.get_value_at(b) >= 0:
        return "No root on this interval"
