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
ELEMENTS_LINE = re.compile("^elements")
DET_LINE = re.compile("^drawElementsTriangles")
DEPTH_LINE = re.compile("^depth")
SRGB_LINE = re.compile("^sRGB")


###########################
# Helpers
###########################
def _parse_parameterized_number_array(per_tuple: int, part_array: list[int | float], cast_type: type, offset=2):
    spot = 0
    pos_tuple = []

    parsed = []

    for pos_part in part_array[offset:]:
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
    print(f'Parsed position array: {state.position}\n')
    state.vals_per_position = per


def handle_color(line: str, state: State):
    parts = line.split()

    if len(parts) < 4:
        raise ValueError(f'Invalid color line: {line}\n')

    per = int(parts[1])
    
    state.color = np.array(_parse_parameterized_number_array(per, parts, float))
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
        dda.draw_triangle([place, place + 1, place + 2], state)
        place += 3

    print(f'Finished drawing triangles from {first} to {first + count}')


def handle_elements(line: str, state: State):
    parts = line.split()

    if len(parts) < 4:
        raise ValueError(f'Invalid elements line: {line}\n')
    
    state.elements = np.array(_parse_parameterized_number_array(1, parts, int, offset=1)).flatten()

    print(f'Finished parsing elements array: {state.elements}\n')


def handle_det(line: str, state: State):
    parts = line.split()

    if len(parts) < 3:
        raise ValueError(f'Invalid drawElementsTriangles line: {line}\n')
    
    count = int(parts[1])
    offset = int(parts[2])

    place = offset
    target = count + offset
    while place < target:
        dda.draw_triangle([state.elements[place], state.elements[place + 1], state.elements[place + 2]], state)
        place = place + 3

    print(f'Finished drawing triangles by elements from {offset} to {target}\n')


def handle_depth(line: str, state: State):
    state.depth = True
    state.depth_buffer = []
    for i in range(state.out_dim_y):
        state.depth_buffer.append([])
        for j in range(state.out_dim_x):
            state.depth_buffer[i].append([])

    print(f'Depth buffer enabled\n')


def handle_srgb(line: str, state: State):
    state.srgb = True

    print(f'sRGB enabled\n')


def get_handler(line: str):
    if PNG_LINE.match(line):
        return handle_png
    elif POSITION_LINE.match(line):
        return handle_pos
    elif COLOR_LINE.match(line):
        return handle_color
    elif DAT_LINE.match(line):
        return handle_dat
    elif ELEMENTS_LINE.match(line):
        return handle_elements
    elif DET_LINE.match(line):
        return handle_det
    elif DEPTH_LINE.match(line):
        return handle_depth
    elif SRGB_LINE.match(line):
        return handle_srgb
    else:
        print(f'Unhandled command: {line}\n')
        return None
    

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


def process_depth_buffer(state: State):
    for y in range(state.out_dim_y):
        for x in range(state.out_dim_x):
            if len(state.depth_buffer[y][x]):
                pixel = sorted(state.depth_buffer[y][x], key=lambda p: p.z_coord)[0]
                state.out_img.im.putpixel((pixel.x_coord, pixel.y_coord), pixel.color)
