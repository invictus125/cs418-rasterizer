from library import should_run, get_handler, write_image
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

write_image(master_state)
