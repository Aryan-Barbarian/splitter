from scipy.spatial import Delaunay
import numpy as np
import math



def memoize(fn):
    known = dict()
    def inner(*args):
        if args not in known:
            known[args] = fn(*args)
        return known[args]
    return inner


def triangularize_points(points):
    """
    Given a list of (x, y) points, returns a list of 
    (a, b, c) triangles
    """
    # print(points)
    tris = [(points[i], points[j], points[k]) for i, j, k in Delaunay(points).simplices]
    return tris


def point_in_triangle (point, triangle):
    # pt = point
    # v1, v2, v3 = triangle
    # b1 = sign(pt, v1, v2) < 0;
    # b2 = sign(pt, v2, v3) < 0;
    # b3 = sign(pt, v3, v1) < 0;
    # if point in triangle:
    #     return True
    Area = triangle_area(triangle)
    px, py = point
    (p0x, p0y), (p1x, p1y), (p2x, p2y)  = triangle

    # if Area == 0:
    #     return False
    s = 1/(2*Area)*(p0y*p2x - p0x*p2y + (p2y - p0y)*px + (p0x - p2x)*py);
    t = 1/(2*Area)*(p0x*p1y - p0y*p1x + (p0y - p1y)*px + (p1x - p0x)*py);
    
    basically_zero = -1e-8
    return s > basically_zero and t > basically_zero and (1 - s - t) > basically_zero

def triangle_centroid(triangle):
    average = lambda nums: sum(nums) / len(nums)
    ans = [ int(average([point[i] for point in triangle])) for i in range(2)]
    ans = tuple(ans)
    return ans


def triangle_area_ratio(triangle):
    a, b, c = triangle
    def distance(p1, p2):
        return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

    side_a = distance(a, b)
    side_b = distance(b, c)
    side_c = distance(c, a)

    s = 0.5 * ( side_a + side_b + side_c)
    area = math.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))

    perimeter = side_a + side_b + side_c

    if (perimeter == 0):
        return float("inf")
    else:
        return area / perimeter

def triangle_area(triangle):
    a, b, c = triangle

    def distance(p1, p2):
        return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

    side_a = distance(a, b)
    side_b = distance(b, c)
    side_c = distance(c, a)
    s = 0.5 * ( side_a + side_b + side_c)
    return math.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))

# points = np.array([[0, 0], [1, 10], [1, 5], [2, 5], [0, 4]])
# tris = triangularize_points(points)
# # print(tris)

# for tri in tris:
#     print (point_in_triangle((0,0), tri))



def sign (p1, p2, p3):
    p1x, p1y = p1
    p2x, p2y = p2
    p3x, p3y = p3

    return (p1x - p3x) * (p2y - p3y) - (p2x - p3x) * (p1y - p3y);

# @memoize
# def triangle_average_color(triangle, readpixels, writepixels):
#     xmin, xmax = min(point[0] for point in triangle), max(point[0] for point in triangle)
#     ymin, ymax = min(point[1] for point in triangle), max(point[1] for point in triangle)

#     total, weight = [0, 0, 0] , 0
#     commonality = dict()
#     for i in range(xmin, xmax):
#         for j in range(ymin, ymax):
#             cpixel = readpixels[i, j]

            
            
#             if point_in_triangle( (i, j), triangle):
#                 weight += 1
#                 total = tuple([(cpixel[i] + total[i]) for i in range(3)])
#     return tuple([int(tot / weight) for tot in total])

# @memoize
# def triangle_total_cost(triangle, readpixels, writepixels):
#     xmin, xmax = min(point[0] for point in triangle), max(point[0] for point in triangle)
#     ymin, ymax = min(point[1] for point in triangle), max(point[1] for point in triangle)

#     total_diff = 0

#     for i in range(xmin, xmax):
#         for j in range(ymin, ymax):
#             cpixel = readpixels[i, j]
#             if point_in_triangle( (i, j), triangle):
#                 new_color = triangle_average_color(triangle, readpixels, writepixels)
#                 total_diff += sum( [abs(cpixel[i] - new_color[i])**2 for i in range(3)] )
    
#     return total_diff