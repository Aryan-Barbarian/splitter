from simpleai.search import SearchProblem, astar
import util
import random
import cacher

class SplitProblem(SearchProblem):

    def __init__(self, initial_state=None, split_image=None):
        self.initial_state = initial_state
        self.split_image = split_image

    def actions(self, state):

        points, time = state
        max_points = self.split_image.max_points
        split_image = self.split_image
        width = split_image.width
        height = split_image.height
        corners= split_image.corners

        def midpoint(a, b):
            average = lambda x, y: (x + y)/2.0
            return (int(average(a[0], b[0])), int(average(a[1], b[1])))

        def valid_point(point):
            x, y = point
            if x < 0 or x >= width:
                return False
            if y < 0 or y >= height:
                return False
            return point not in points

        triangles = util.triangularize_points(points)
        ans = []

        
        if len(points) < max_points:
            for triangle in triangles:
                if util.triangle_area(triangle) < 60:
                    continue

                a, b, c = triangle

                mid = midpoint(a, b)
                if valid_point(mid):
                    ans.append( ("ADD", mid) )

                mid = midpoint(a, c)
                if valid_point(mid):
                    ans.append( ("ADD", mid) )

                mid = midpoint(c, b)
                if valid_point(mid):
                    ans.append( ("ADD", mid) )

                centroid = util.triangle_centroid(triangle)
                if valid_point(centroid):
                    ans.append( ("ADD", centroid))

        for point in points:
            if point in corners:
                continue

            x, y = point

            for i in range(-1, 2):
                for j in range(-1, 2):
                    for d in [4**k for k in range(0, 2)]:
                        p = (x + d * i, y + d * j)
                        if valid_point( p ) and p != point:
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

    def generate_random_state(self):
        corners = self.split_image.corners
        max_points = self.split_image.max_points
        points = [] + corners
        while len(points) < max_points - 10:
            point = self.random_point()
            if point not in points:
                points.append(point)
        return (points, 0)

    def result(self, state, action):
        points, time = state

        if action[0] == "MOVE":
            original = action[1]
            new_point = action[2]
            points = [p for p in points if p != original]
            points.append(new_point)
            points = sorted(points)
            points = tuple(points)
        elif action[0] == "ADD":

            # new_point = self.random_point()
            new_point = action[1]
            points = list(points)
            points.append(new_point)
            points = sorted(points)
            points = tuple(points)

        new_state = points, time + 1
        return new_state


    def value(self, state):
        points = state[0]
        time = state[1]

        if time > 500:
            return float("-inf")

        triangles = util.triangularize_points(points)
        average_colors = {tri : ((0, 0, 0) , 0) for tri in triangles}

        total_diff = 0
        split_image = self.split_image
        readpixels = split_image.readpixels
        writepixels = split_image.writepixels
        max_points = split_image.max_points
        best = split_image.best
        use_color_mask = split_image.shrink_factor != 1

        for triangle in triangles:

            to_add = split_image.triangle_total_cost(triangle, use_color_mask)

            total_diff += to_add

        val = -total_diff
        # print(val, best["value"])
        if val > best["value"]:
            best["value"] = val
            best["path"] = state
            # display(points)
            print(time, val, state)
            cacher.log(split_image.image_name, state, val)

        unused_points = max_points - len(points)

        penalty = 5000 * unused_points
        penalty = 0
        return -1 * total_diff + penalty

    def is_goal(self, state):
        points, time = state
        val = self.value(state)
        return val > -336967818

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        return self.value(state)
