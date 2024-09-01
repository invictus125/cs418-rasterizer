from state import State
import numpy as np
from math import ceil


class DDAEdge:
    def __init__(
            self,
            end1: list[float], # Point to step from
            end2: list[float], # Point to step toward
            step_dimension: int, # Which dimension to step along
    ):
        self.end1 = np.array(end1)
        self.end2 = np.array(end2)
        self.step_dimension = step_dimension

        # Calculate step vector
        self.step_direction = 1 if self.end2[step_dimension] > self.end1[step_dimension] else -1
        self.step_vector = self.step_direction * np.array(
            np.subtract(self.end1, self.end2)
            / (self.end1[self.step_dimension] - self.end2[self.step_dimension])
        )

        # Calculate and apply offset
        offset_vector = (ceil(self.end1[self.step_dimension]) - self.end1[self.step_dimension]) * self.step_vector
        self.spot = np.add(self.end1, offset_vector)
        
    def step(self):
        self.spot = np.add(self.spot, self.step_vector)
        if (
            (self.step_direction < 0 and self.spot[self.step_dimension] < self.end2[self.step_dimension])
            or
            (self.step_direction > 0 and self.spot[self.step_dimension] > self.end2[self.step_dimension])
        ):
            return None
        
        return self.spot
    
    def get_goal_end(self):
        return self.end2
    
    def get_current_point(self):
        return self.spot


def scan_line(left, right, colors, state: State):
    if left[0] == right[0]:
        return

    x_edge = DDAEdge(left, right, 0)
    spot = x_edge.get_current_point()

    # Traverse horizontally and find pixel coords
    while spot is not None:
        print(f'pixel found: ({spot[0]}, {left[1]})')

        # TODO: interpolate color


        # state.out_img.im.putpixel((spot[0], left[1]), (r,g,b,a))

        spot = x_edge.step()


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

    print(f'TB: {tb}\nTM: {tm}\nMB: {mb}')

    if tb[0][0] < tm[0][0]:
        left_edge = DDAEdge(tb[1], tb[0], 1)
        right_edge = DDAEdge(tm[1], tm[0], 1)
        print('left edge is tb')
    else:
        left_edge = DDAEdge(tm[1], tm[0], 1)
        right_edge = DDAEdge(tb[1], tb[0], 1)
        print('left edge is tm')

    # Get starting spots after offset is applied
    spot_left = left_edge.get_current_point()
    spot_right = right_edge.get_current_point()

    print(f'start points: <- {spot_left} and -> {spot_right}')

    corner_turned = False
    while spot_left is not None and spot_right is not None:
        scan_line(spot_left, spot_right, colors, state)

        spot_left = left_edge.step()
        spot_right = right_edge.step()

        # Turn the corner if needed
        if not corner_turned and spot_left is None:
            left_edge = DDAEdge(mb[1], mb[0], 1)
            spot_left = left_edge.get_current_point()
            corner_turned = True
            print('corner turned on left')
        elif not corner_turned and spot_right is None:
            right_edge = DDAEdge(mb[1], mb[0], 1)
            spot_right = right_edge.get_current_point()
            corner_turned = True
            print('corner turned on right')
