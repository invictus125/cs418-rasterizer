from PIL import Image


class Pixel:
    x_coord: int
    y_coord: int
    z_coord: int
    color: list[int]


class State:
    out_img: Image
    out_file_name: str
    out_dim_x: int
    out_dim_y: int
    position: list[list[float]]
    vals_per_position: int
    color: list[list[int]]
    elements: list[int]
    vals_per_color: int
    depth: bool
    depth_buffer: list[list[list[Pixel]]]
    srgb: bool
    hyp: bool

    def __init__(self):
        self.depth = False
        self.srgb = False
        self.hyp = False
