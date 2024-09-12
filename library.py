import re
from PIL import Image
import dda
from state import State
import numpy as np


###########################
# Regexes
###########################
EMPTY_LINE = re.compile("^\s*$")
COMMENT_LINE = re.compile("^#")
PNG_LINE = re.compile("^png\s")
DAT_LINE = re.compile("^drawArraysTriangles")
COLOR_LINE = re.compile("^color")
POSITION_LINE = re.compile("^position")


###########################
# Helpers
###########################
def _parse_parameterized_number_array(per_tuple: int, part_array: list[int | float], cast_type: type):
    spot = 0
    pos_tuple = []

    parsed = []

    for pos_part in part_array[2:]:
        if spot >= per_tuple:
            parsed.append(pos_tuple.copy())
            pos_tuple = []
            spot = 0

        pos_tuple.append(cast_type(pos_part))
        spot += 1

    if len(pos_tuple):
        parsed.append(pos_tuple)

    return parsed


def _apply_screen_coords(points: list[list[float]], x_size: int, y_size: int):
    points = np.array(points)
    for idx in range(np.shape(points)[1]):
        point = points[idx][:]
        
        # Divide by w
        w = point[3] if len(point) == 4 else 1
        point[0] = point[0] / w
        point[1] = point[1] / w

        # Move X and Y coords according to the available viewport
        point[0] = ((point[0] + 1) / 2) * x_size
        point[1] = ((point[1] + 1) / 2) * y_size

        points[idx] = point

    print(f'After apply screen coords: {points}')
    return points


###########################
# Command handlers
###########################
def handle_png(line: str, state: State):
    parts = line.split()

    if len(parts) < 4:
        raise ValueError(f'Invalid PNG line: {line}\n')
    
    state.out_dim_x = int(parts[1])
    state.out_dim_y = int(parts[2])
    state.out_file_name = parts[3]
    state.out_img = Image.new("RGBA", (state.out_dim_x, state.out_dim_y), (0,0,0,0))


def handle_pos(line: str, state: State):
    parts = line.split()

    if len(parts) < 5:
        raise ValueError(f'Invalid position line: {line}\n')

    per = int(parts[1])
    
    init_position = _parse_parameterized_number_array(per, parts, float)
    print(f'Parsed position array: {init_position}\n')
    state.position = _apply_screen_coords(
        np.array(init_position),
        state.out_dim_x,
        state.out_dim_y,
    )
    state.vals_per_position = per


def handle_color(line: str, state: State):
    parts = line.split()

    if len(parts) < 4:
        raise ValueError(f'Invalid color line: {line}\n')

    per = int(parts[1])
    
    state.color = np.array(_parse_parameterized_number_array(per, parts, int))
    state.vals_per_color = per

    print(f'Finished parsing color array: {state.color}\n')


def handle_dat(line: str, state: State):
    parts = line.split()

    if len(parts) < 3:
        raise ValueError(f'Invalid drawArraysTriangles line: {line}\n')

    first = int(parts[1])
    count = int(parts[2])

    place = first
    while place < (first + count):
        dda.draw_triangle(place, state)
        place += 3

    print(f'Finished drawing triangles from {first} to {first + count}')


def get_handler(line: str):
    if PNG_LINE.match(line):
        return handle_png
    elif POSITION_LINE.match(line):
        return handle_pos
    elif COLOR_LINE.match(line):
        return handle_color
    elif DAT_LINE.match(line):
        return handle_dat
    else:
        raise ValueError(f'Unhandled command: {line}\n')
    

###########################
# Helpers
###########################
def should_run(line: str) -> bool:
    if EMPTY_LINE.match(line):
        return False

    if COMMENT_LINE.match(line):
        return False

    return True


def write_image(state: State):
    filename = state.out_file_name
    state.out_img.save(filename)
    print(f'Wrote {filename}')
