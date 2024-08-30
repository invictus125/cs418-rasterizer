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
    
    state.position = np.array(_parse_parameterized_number_array(per, parts, float))

    print(f'Finished parsing position array: {state.position}\n')


def handle_color(line: str, state: State):
    parts = line.split()

    if len(parts) < 4:
        raise ValueError(f'Invalid color line: {line}\n')

    per = int(parts[1])
    
    state.color = np.array(_parse_parameterized_number_array(per, parts, int))

    print(f'Finished parsing color array: {state.color}\n')


def handle_dat(line: str, state: State):
    parts = line.split()

    if len(parts) < 3:
        raise ValueError(f'Invalid drawArraysTriangles line: {line}\n')

    first = int(parts[1])
    count = int(parts[2])

    place = first
    while place < count:
        dda.draw_triangle(place, state)
        place += 3

    print(f'Finished drawing triangles from {first} to {count}')


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
