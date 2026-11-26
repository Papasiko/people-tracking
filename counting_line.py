LINE_START = (600, 500)
LINE_END = (1000, 500)
LINE_Y = LINE_START[1]


def crosses_counting_line(previous_position, current_position):
    """Return True when a tracked foot point crosses the visible line top-to-bottom."""
    previous_x, previous_y = previous_position
    current_x, current_y = current_position

    if not (previous_y < LINE_Y <= current_y):
        return False

    delta_y = current_y - previous_y
    if delta_y == 0:
        return False

    # Interpolate the X coordinate at the exact frame-to-frame crossing point.
    crossing_ratio = (LINE_Y - previous_y) / delta_y
    crossing_x = previous_x + crossing_ratio * (current_x - previous_x)

    line_min_x, line_max_x = sorted((LINE_START[0], LINE_END[0]))
    return line_min_x <= crossing_x <= line_max_x
