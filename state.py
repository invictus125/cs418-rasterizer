from PIL import Image

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
