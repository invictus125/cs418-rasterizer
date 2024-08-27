import re
from PIL import Image
import dda


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
# State constant names
###########################
OUT_IMAGE = "outimg"
OUT_FILE_NAME = "outname"
OUT_DIM_X = "outdimx"
OUT_DIM_Y = "outdimy"


###########################
# Command handlers
###########################
def handle_png(line: str, state: dict):
    parts = line.split()

    if len(parts) < 4:
        raise ValueError(f'Invalid PNG line: {line}')
    
    state[OUT_DIM_X] = int(parts[1])
    state[OUT_DIM_Y] = int(parts[2])
    state[OUT_FILE_NAME] = parts[3]
    state[OUT_IMAGE] = Image.new("RGBA", (state[OUT_DIM_X], state[OUT_DIM_Y]), (0,0,0,0))


def handle_pos(line: str, state: dict):
    raise NotImplementedError()


def handle_color(line: str, state: dict):
    raise NotImplementedError()


def handle_dat(line: str, state: dict):
    raise NotImplementedError()


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
        raise ValueError(f'Unhandled command: {line}')
    

###########################
# Helpers
###########################
def should_run(line: str) -> bool:
    if EMPTY_LINE.match(line):
        return False

    if COMMENT_LINE.match(line):
        return False

    return True


def write_image(state: dict):
    filename = state.get(OUT_FILE_NAME)
    state.get(OUT_IMAGE).save(filename)
    print(f'Wrote {filename}')
