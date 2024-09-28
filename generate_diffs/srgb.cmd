magick compare -fuzz 2% ../sRGB.png ../correct_outputs/rast-sRGB.png sRGB_compare.png
magick composite ../sRGB.png ../correct_outputs/rast-sRGB.png -alpha off -compose difference sRGB_rawdiff.png
magick convert sRGB_rawdiff.png -level 0%,8% sRGB_diff.png
magick convert +append ../correct_outputs/rast-sRGB.png ../sRGB.png sRGB_compare.png sRGB_rawdiff.png sRGB_diff.png ../sRGB_full_diff.png
del sRGB_compare.png
del sRGB_rawdiff.png
del sRGB_diff.png