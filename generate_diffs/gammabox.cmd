magick compare -fuzz 2% ../gammabox.png ../correct_outputs/rast-gammabox.png gammabox_compare.png
magick composite ../gammabox.png ../correct_outputs/rast-gammabox.png -alpha off -compose difference gammabox_rawdiff.png
magick convert gammabox_rawdiff.png -level 0%,8% gammabox_diff.png
magick convert +append ../correct_outputs/rast-gammabox.png ../gammabox.png gammabox_compare.png gammabox_rawdiff.png gammabox_diff.png ../gammabox_full_diff.png
del gammabox_compare.png
del gammabox_rawdiff.png
del gammabox_diff.png