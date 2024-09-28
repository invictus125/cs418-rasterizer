magick compare -fuzz 2% ../oldlogo.png ../correct_outputs/rast-elements.png elements_compare.png
magick composite ../oldlogo.png ../correct_outputs/rast-elements.png -alpha off -compose difference elements_rawdiff.png
magick convert elements_rawdiff.png -level 0%,8% elements_diff.png
magick convert +append ../correct_outputs/rast-elements.png ../oldlogo.png elements_compare.png elements_rawdiff.png elements_diff.png ../elements_full_diff.png
del elements_compare.png
del elements_rawdiff.png
del elements_diff.png
