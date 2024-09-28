magick compare -fuzz 2% ../depth.png ../correct_outputs/rast-depth.png depth_compare.png
magick composite ../depth.png ../correct_outputs/rast-depth.png -alpha off -compose difference depth_rawdiff.png
magick convert depth_rawdiff.png -level 0%,8% depth_diff.png
magick convert +append ../correct_outputs/rast-depth.png ../depth.png depth_compare.png depth_rawdiff.png depth_diff.png ../depth_full_diff.png
del depth_compare.png
del depth_rawdiff.png
del depth_diff.png