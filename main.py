from math import ceil, floor, modf, sqrt
from PIL import Image
import numpy as np
import struct

img = np.array(Image.open("./catbaby.png").convert("RGBA"), dtype=np.float32)

out = b"\x03\x00\x00\x00"
(w, h, chan) = img.shape
basex = sqrt(3) / 2
basey = 1 / 2


def inrange(a):
    return max(0, min(w - 1, a))


def sample(x, y):
    lx, hx, ly, hy = (
        inrange(floor(x)),
        inrange(ceil(x)),
        inrange(floor(y)),
        inrange(ceil(y)),
    )
    (rx, _), (ry, _) = modf(x), modf(y)
    return (
        img[lx, ly] * (1 - rx) * (1 - ry)
        + img[hx, ly] * rx * (1 - ry)
        + img[lx, hy] * (1 - rx) * ry
        + img[hx, hy] * rx * ry
    )


sx, bx = -floor(h * basex / basey), w
sy, by = 0, floor(h / basey)
out += struct.pack("<I", (bx - sx) * (by - sy))
out += b"\x03\x00\x00\x00"
for x in range(sx, bx):
    for y in range(sy, by):
        out += b"BODY"
        col = sample(x + basex * y, basey * y) / 255
        out += struct.pack("<4f", *col)
        out += struct.pack("<i", y)
        out += struct.pack("<i", x)
open("out.bod", "wb").write(out)
