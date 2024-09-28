make run file=test_input/rast-gray.txt > gray_out
make run file=test_input/rast-smallgap.txt > smallgap_out
make run file=test_input/rast-smoothcolor.txt > smoothcolor_out
make run file=test_input/rast-checkers.txt > checkers_out
make run file=test_input/rast-elements.txt > elements_out
make run file=test_input/rast-depth.txt > depth_out
make run file=test_input/rast-perspective.txt > perspective_out
make run file=test_input/rast-sRGB.txt > srgb_out
make run file=test_input/rast-gammabox.txt > gammabox_out

cd generate_diffs

start cmd.exe /c checkers.cmd
start cmd.exe /c elements.cmd
start cmd.exe /c gammabox.cmd
start cmd.exe /c gray.cmd
start cmd.exe /c perspective.cmd
start cmd.exe /c smallgap.cmd
start cmd.exe /c smoothcolor.cmd
start cmd.exe /c srgb.cmd
start cmd.exe /c depth.cmd

cd ..