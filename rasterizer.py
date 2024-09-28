from library import should_run, get_handler, write_image, process_depth_buffer
from state import State
import sys

# Vars
master_state = State()

lines = []
with open(sys.argv[1]) as file:
    for line in file:
        line = line.strip()
        if should_run(line):
            print(line)
            handler = get_handler(line)
            if handler is not None:
                handler(line, master_state)

    file.close()

if master_state.depth:
    process_depth_buffer(master_state)

write_image(master_state)
