build:
	echo Done

run:
	python3 ./rasterizer.py $(file)

cleanWin:
	del "*_out"
	del "*.png"
