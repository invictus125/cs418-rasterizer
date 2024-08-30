from state import State
import numpy as np
from math import ceil


def scan_line(left, right, colors, state: State):
    d_vec = np.subtract(right, left) / (right[0] - left[0])
    o_vec = (ceil(left[0]) - left[0]) * d_vec

    # Apply offset
    spot = np.add(np.copy(left), o_vec)

    # Traverse horizontally and find pixel coords
    while spot[0] < right[0]:
        print(f'pixel found: ({spot[0]}, {left[1]})')

        # TODO: interpolate color

        # TODO: write pixel into state png

        spot = spot + d_vec


def draw_triangle(place: int, state: State):
    points = state.position[place:place+3]
    colors = state.color[place:place+3]

    p1 = points[0,:]
    p2 = points[1,:]
    p3 = points[2,:]

    # Construct edges of triangle in order of y-values:
    # tb = top to bottom
    # mb = middle to bottom
    # tm = top to middle
    sorted_points = sorted([p1, p2, p3], key=lambda p: p[1])
    tb = [sorted_points[0], sorted_points[2]]
    mb = [sorted_points[0], sorted_points[1]]
    tm = [sorted_points[1], sorted_points[2]]

    # Calculate unit vectors in Y-direction
    d_vec_tb = np.subtract(tb[1], tb[0]) / (tb[1][1] - tb[0][1])
    d_vec_mb = np.subtract(mb[1], mb[0]) / (mb[1][1] - mb[0][1])
    d_vec_tm = np.subtract(tm[1], tm[0]) / (tm[1][1] - tm[0][1])

    # Calculate offset vectors (from top)
    o_vec_tb = (ceil(tb[1][1]) - tb[1][1]) * d_vec_tb
    o_vec_mb = (ceil(mb[1][1]) - mb[1][1]) * d_vec_mb
    o_vec_tm = (ceil(tm[1][1]) - tm[1][1]) * d_vec_tm

    # Apply offsets
    tb[1] = np.subtract(tb[1], o_vec_tb)
    mb[1] = np.subtract(mb[1], o_vec_mb)
    tm[1] = np.subtract(tm[1], o_vec_tm)

    # Find integer y-values along triangle edges
    left_edge = tb if tb[0][0] < tm[0][0] else tm
    left_step = d_vec_tb if tb[0][0] < tm[0][0] else d_vec_tm
    right_edge = tb if tb[0][0] >= tm[0][0] else tm
    right_step = d_vec_tb if tb[0][0] >= tm[0][0] else d_vec_tm
    spot_left = left_edge[1]
    spot_right = right_edge[1]
    while spot_left[1] >= tb[0][1]:
        scan_line(spot_left, spot_right, colors, state)
        spot_left = np.subtract(spot_left, left_step)
        spot_right = np.subtract(spot_right, right_step)

        # Turn the corner if needed
        if spot_left[1] < left_edge[0][1]:
            left_edge = mb
            left_step = d_vec_mb
        elif spot_right[1] < right_edge[0][1]:
            right_edge = mb
            right_step = d_vec_mb
