magick compare -fuzz 2% ../checkers.png ../correct_outputs/rast-checkers.png checkers_compare.png
magick composite ../checkers.png ../correct_outputs/rast-checkers.png -alpha off -compose difference checkers_rawdiff.png
magick convert checkers_rawdiff.png -level 0%,8% checkers_diff.png
magick convert +append ../correct_outputs/rast-checkers.png ../checkers.png checkers_compare.png checkers_rawdiff.png checkers_diff.png ../checkers_full_diff.png
del checkers_compare.png
del checkers_rawdiff.png
del checkers_diff.png