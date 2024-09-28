magick compare -fuzz 2% ../gray.png ../correct_outputs/rast-gray.png gray_compare.png
magick composite ../gray.png ../correct_outputs/rast-gray.png -alpha off -compose difference gray_rawdiff.png
magick convert gray_rawdiff.png -level 0%,8% gray_diff.png
magick convert +append ../correct_outputs/rast-gray.png ../gray.png gray_compare.png gray_rawdiff.png gray_diff.png ../gray_full_diff.png
del gray_compare.png
del gray_rawdiff.png
del gray_diff.png