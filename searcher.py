from simpleai.search import SearchProblem, astar
import util
import random
import cacher

class SplitProblem(SearchProblem):

    def __init__(self, initial_state=None, split_image=None):
        self.initial_state = initial_state
        self.split_image = split_image

    def actions(self, state):

        triangle_mask = state
        max_points = self.split_image.max_points
        split_image = self.split_image
        width = split_image.width
        height = split_image.height
        corners = split_image.corners

        # def midpoint(a, b):
        #     average = lambda x, y: (x + y)/2.0
        #     return (int(average(a[0], b[0])), int(average(a[1], b[1])))

        ans = []
        triangles = triangle_mask.triangles
        points = triangle_mask.points

        if len(points) < max_points:
            for triangle in triangles:
                if util.triangle_area(triangle) < 50:
                    continue
                
                center = util.triangle_centroid(triangle)
                if center not in triangle:
                    ans.append( ("SHATTER", triangle) )

        for point in points:
            # print(points, point)
            if point in corners:
                continue
            
            x, y = point

            for i in range(-1, 2):
                for j in range(-1, 2):
                    for d in [3**k for k in range(0, 1)]:
                        p = (x + d * i, y + d * j)
                        if triangle_mask.legal_move(point, p):
                            ans.append( ("MOVE", point, p) )
        random.shuffle(ans)
        return ans

    def random_point(self):
        split_image = self.split_image
        width = split_image.width
        height = split_image.height
        
        x = random.randint(1, width - 1)
        y = random.randint(1, height - 1)
        point = (x, y)
        return point

    # def generate_random_state(self):
    #     corners = self.split_image.corners
    #     max_points = self.split_image.max_points
    #     points = [] + corners
    #     while len(points) < max_points - 10:
    #         point = self.random_point()
    #         if point not in points:
    #             points.append(point)
    #     return (points, 0)

    def result(self, state, action):
        triangle_mask = state

        if action[0] == "MOVE":
            original = action[1]
            new_point = action[2]
            new_state = triangle_mask.move_point(original, new_point)
        elif action[0] == "SHATTER":

            # new_point = self.random_point()
            triangle = action[1]
            new_state = triangle_mask.shatter_triangle(triangle)

        return new_state


    def value(self, state):
        triangle_mask = state
        triangles = triangle_mask.triangles
        points = triangle_mask.points

        average_area = sum(map(util.triangle_area, triangles)) / len(triangles)

        total_diff = 0
        split_image = self.split_image
        readpixels = split_image.readpixels
        writepixels = split_image.writepixels
        max_points = split_image.max_points
        best = split_image.best
        use_color_mask = split_image.shrink_factor != 1

        for triangle in triangles:

            to_add = split_image.triangle_total_cost(triangle, use_color_mask)

            area = util.triangle_area(triangle)
            area_cost = max(0, ((average_area*0.35 - area) * 60000))
            total_diff += to_add + area_cost

        val = -total_diff
        if val > best["value"]:
            best["value"] = val
            best["path"] = state
            # display(points)
            print(val, points)
            cacher.log(split_image.image_name, state, val)

        unused_points = max_points - len(points)

        penalty = 5000 * unused_points
        penalty = 0
        return -1 * total_diff + penalty

    # def is_goal(self, state):
    #     points, time = state
    #     val = self.value(state)
    #     return val > -336967818

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        return self.value(state)
