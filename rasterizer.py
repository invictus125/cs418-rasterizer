from library import should_run, get_handler, write_image, process_depth_buffer
from state import State
import sys

# Vars
master_state = State()

lines = []
with open(sys.argv[1]) as file:
    for line in file:
        if should_run(line):
            print(line)
            get_handler(line)(line, master_state)

    file.close()

if master_state.depth:
    process_depth_buffer(master_state)

write_image(master_state)
