magick compare -fuzz 2% ../smoothcolor.png ../correct_outputs/rast-smoothcolor.png smoothcolor_compare.png
magick composite ../smoothcolor.png ../correct_outputs/rast-smoothcolor.png -alpha off -compose difference smoothcolor_rawdiff.png
magick convert smoothcolor_rawdiff.png -level 0%,8% smoothcolor_diff.png
magick convert +append ../correct_outputs/rast-smoothcolor.png ../smoothcolor.png smoothcolor_compare.png smoothcolor_rawdiff.png smoothcolor_diff.png ../smoothcolor_full_diff.png
del smoothcolor_compare.png
del smoothcolor_rawdiff.png
del smoothcolor_diff.png