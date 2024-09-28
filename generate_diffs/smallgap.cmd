magick compare -fuzz 2% ../smallgap.png ../correct_outputs/rast-smallgap.png smallgap_compare.png
magick composite ../smallgap.png ../correct_outputs/rast-smallgap.png -alpha off -compose difference smallgap_rawdiff.png
magick convert smallgap_rawdiff.png -level 0%,8% smallgap_diff.png
magick convert +append ../correct_outputs/rast-smallgap.png ../smallgap.png smallgap_compare.png smallgap_rawdiff.png smallgap_diff.png ../smallgap_full_diff.png
