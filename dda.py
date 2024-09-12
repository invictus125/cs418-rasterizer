from state import State
import numpy as np
from math import ceil


def _get_color(vector: list[float], state):
    offset = state.vals_per_position
    color_length = state.vals_per_color

    a = 255
    if color_length == 4:
        a = round(vector[offset + 3] * 255)

    return (round(vector[offset] * 255), round(vector[offset+1] * 255), round(vector[offset+2] * 255), a)


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
        if abs(self.end2[self.step_dimension] - self.end1[self.step_dimension]) <= 0.001:
            # Handle case where there is no step needed and avoid divide by zero
            vec_shape = np.shape(self.end2)
            self.step_vector = np.zeros(vec_shape)
            offset_vector = np.zeros(vec_shape)
            offset_vector[step_dimension] = ceil(self.end1[self.step_dimension]) - self.end1[self.step_dimension]
        else:
            self.step_vector = self.step_direction * np.array(
                np.subtract(self.end2, self.end1)
                / (self.end2[self.step_dimension] - self.end1[self.step_dimension])
            )
            
            # Calculate and apply offset
            offset_vector = (ceil(self.end1[self.step_dimension]) - self.end1[self.step_dimension]) * self.step_vector

        
        self.spot = np.add(self.end1, offset_vector)


    def step(self):
        original_pos_step_dim = self.spot[self.step_dimension]
        self.spot = np.add(self.spot, self.step_vector)
        if (
            # Check whether we're beyond the end point
            (self.step_direction > 0 and self.spot[self.step_dimension] > self.end2[self.step_dimension])
            or
            (self.step_direction < 0 and self.spot[self.step_dimension] < self.end2[self.step_dimension])
            or
            # Check whether we failed to move with the step operation
            (self.spot[self.step_dimension] == original_pos_step_dim)
        ):
            # Returning None signals that no more steps are possible
            return None
        
        return self.spot
    
    def get_goal_end(self):
        return self.end2
    
    def get_current_point(self):
        return self.spot


def scan_line(left, right, state: State):
    y_val = int(left[1])

    print(f'scan_line: Scanning {left} -> {right}')
    if left[0] == right[0] or y_val >= state.out_dim_y:
        return

    x_edge = DDAEdge(left, right, 0)
    spot = x_edge.get_current_point()

    # Traverse horizontally and find pixel coords
    
    while spot is not None:
        x_val = int(spot[0])

        # Sanity-check image bounds
        if x_val >= state.out_dim_x:
            break

        color = _get_color(spot, state)

        # print(f'\tpixel found: ({x_val}, {y_val}) -> {color}')

        state.out_img.im.putpixel((x_val, y_val), color)

        spot = x_edge.step()


def draw_triangle(place: int, state: State):
    points = state.position[place:place+3]
    colors = state.color[place:place+3]
    print(f'draw_triangle: drawing with points {points} and colors {colors}')

    # Combine points and colors so we can interpolate them as one operation
    p1 = np.concatenate([points[0], colors[0]])
    p2 = np.concatenate([points[1], colors[1]])
    p3 = np.concatenate([points[2], colors[2]])

    # Construct edges of triangle in order of y-values:
    # tb = top to bottom
    # mb = middle to bottom
    # tm = top to middle
    sorted_points = sorted([p1, p2, p3], key=lambda p: p[1])
    tb = [sorted_points[0], sorted_points[2]]
    mb = [sorted_points[1], sorted_points[2]]
    tm = [sorted_points[0], sorted_points[1]]

    print(f'draw_triangle: edges\n\tTB: {tb}\n\tTM: {tm}\n\tMB: {mb}')

    if tb[1][0] < tm[1][0]:
        left_edge = DDAEdge(tb[0], tb[1], 1)
        right_edge = DDAEdge(tm[0], tm[1], 1)
        print('draw_triangle: left edge is tb, right edge is tm')
    else:
        left_edge = DDAEdge(tm[0], tm[1], 1)
        right_edge = DDAEdge(tb[0], tb[1], 1)
        print('draw_triangle: left edge is tm, right edge is tb')

    # Get starting spots after offset is applied
    spot_left = left_edge.get_current_point()
    spot_right = right_edge.get_current_point()

    corner_turned = False
    while spot_left is not None and spot_right is not None:
        scan_line(spot_left, spot_right, state)

        spot_left = left_edge.step()
        spot_right = right_edge.step()

        # Turn the corner if needed
        if not corner_turned and spot_left is None:
            left_edge = DDAEdge(mb[0], mb[1], 1)
            spot_left = left_edge.get_current_point()
            corner_turned = True
            print('draw_triangle: corner turned on left')
        elif not corner_turned and spot_right is None:
            right_edge = DDAEdge(mb[0], mb[1], 1)
            spot_right = right_edge.get_current_point()
            corner_turned = True
            print('draw_triangle: corner turned on right')
