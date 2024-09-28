magick compare -fuzz 2% ../perspective.png ../correct_outputs/rast-perspective.png perspective_compare.png
magick composite ../perspective.png ../correct_outputs/rast-perspective.png -alpha off -compose difference perspective_rawdiff.png
magick convert perspective_rawdiff.png -level 0%,8% perspective_diff.png
magick convert +append ../correct_outputs/rast-perspective.png ../perspective.png perspective_compare.png perspective_rawdiff.png perspective_diff.png ../perspective_full_diff.png
del perspective_compare.png
del perspective_rawdiff.png
del perspective_diff.png