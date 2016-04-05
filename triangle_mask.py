import util

def replace_triangle_point(self, triangle, old_point, new_point):
    return tuple( [point if point != old_point else new_point for point in triangle] )

def clockwise_triangle(triangle):
    p1, p2, p3 = triangle

    # if p1[0] == p2[0]:
    #     p1, p2, p3 = p1, p3, p2

    # if (p1[0] <= p2[0] and p2[1] <= p3[1] ) or (p1[0] >= p2[0] and p2[1] >= p3[1]):
    #     return triangle
    # else:
    #     return p3, p2, p1
    total = 0
    for i in range(len(triangle)):
        j = (i + 1) % len(triangle)
        total += (triangle[j][0] - triangle[i][0])*(triangle[j][1] + triangle[i][1])

    if total > 0:
        return (p3, p2, p1)
    else:
        return (p1, p2, p3)

class TriangleMask(object):
    """docstring for TriangleMask"""
    def __init__(self, width, height, triangles=None, points=None, dict_cache=None):
        self.corners = self.generate_corners(width, height)
        self.width = width
        self.height = height
        if (dict_cache is not None):
            points = dict_cache["POINTS"]
            triangles = dict_cache["TRIANGLES"]

        if points is None:
            points = self.get_initial_points()
        
        if triangles is None:
            triangles = util.triangularize_points(points)


        triangles = [clockwise_triangle(tri) for tri in triangles]

        self.triangles = tuple(triangles)
        self.points = tuple(points)
        self.width = width
        self.height = height

    def get_initial_points(self):
        ans = list()
        ans.extend(self.corners)
        for i in range(1, self.width - 5, 30):
            for j in range(1, self.height - 5, 30):
                ans.append( (i, j) )
        return ans

    def inclusive_triangles(self, point):
        ans = []
        for triangle in self.triangles:
            if util.point_in_triangle(point, triangle):
                ans.append(triangle)
        return ans

    def legal_move(self, old_point, new_point):
        if old_point in self.corners or new_point in self.points:
            return False

        if old_point == new_point:
            return False
        
        x, y = new_point

        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False

        new_triangles = self.inclusive_triangles(new_point)
        
        if len(new_triangles) != 1:
            ans = False
        else: 
            old_triangles = self.inclusive_triangles(old_point)
            for triangle in old_triangles:
                if util.triangle_area(triangle) < 25:
                    return False
            ans = new_triangles[0] in old_triangles
        return ans

    def generate_corners(self, width, height):
        return tuple([ (0, 0), (width, 0), (0, height), (width, height)])

    def move_point(self, old_point, new_point):
        # TODO: What if this causes triangles to intersect?
        if new_point in self.points:
            return False

        
        replace_point = lambda point: point if point != old_point else new_point
        replace_triangle = lambda triangle: tuple(map(replace_point, triangle))

        new_triangles = tuple(map(replace_triangle, self.triangles))
        new_points = tuple(map(replace_point, self.points))

        return TriangleMask(self.width, self.height, new_triangles, new_points)


    def shatter_triangle(self, triangle):
        new_triangles = []
        new_points = list(self.points)
        a, b, c = triangle
        for tri in self.triangles:
            if tri != triangle:
                new_triangles.append(tri)
                continue 
            
            center = util.triangle_centroid(triangle)

            new_triangles.append( (a, b, center) )
            new_triangles.append( (a, c, center) )
            new_triangles.append( (c, b, center) )
            new_points.append( center )
        new_points = tuple(new_points)
        return TriangleMask(self.width, self.height, new_triangles, new_points)





        
        