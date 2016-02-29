import util
from PIL import Image
from searcher import SplitProblem
from simpleai.search import beam, breadth_first, astar, greedy, hill_climbing_random_restarts,\
 limited_depth_first, hill_climbing, hill_climbing_stochastic

filepath = "images/panda-sm.png"


MAX_POINTS = 120
JUMP_FAR = 5
JUMP_CLOSE = 1
COLORFLAT = 1

class SplitImage(object):
    def __init__(self, filepath, max_points):
        self.max_points = max_points
        self.img, readonly = self.load_image(filepath), self.load_image(filepath)
        self.width, self.height = self.img.size
        self.corners = [ (0,0), (self.width, 0), (0, self.height), (self.width, self.height) ]
        self.readpixels = readonly.load()
        self.writepixels = self.img.load()
        self.best = {"value":float("-inf")}

    def pixelize_image(self):
        points = [] + self.corners

        my_problem = SplitProblem( (tuple(points), 0), self )

        # result = astar(my_problem, graph_search = True)
        # result = limited_depth_first(my_problem, 5)
        # result = beam(my_problem, beam_size = 100)
        # result = hill_climbing_random_restarts(my_problem, 2)
        result = hill_climbing(my_problem)

        print("FINAL RESULT REACHED")
        print("RESULT: {}".format(result.state[0]))
        print("SCORE: {}".format(my_problem.value(result.state)))
        print("PATH: {}".format(result.path()))

        points = result.state[0]
        self.display(points)


    def load_image(self, filepath):
        im = Image.open(filepath)
        im = im.convert('RGB')
        return im

    def display(self, points):
        triangles = util.triangularize_points(points)

        for i in range(self.width):
            for j in range(self.height):
                cpixel = self.readpixels[i, j]
                for tri in triangles:
                    if util.point_in_triangle( (i, j), tri):
                        new_average = util.triangle_average_color(tri, self.readpixels, self.writepixels)
                        cpixel = new_average

                self.writepixels[i, j] = cpixel
        self.img.show()



def main():
    split_image = SplitImage("images/panda-sm.png", 5)
    split_image.pixelize_image()

if __name__ == "__main__":
    main()