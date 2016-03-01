import util
from PIL import Image
from searcher import SplitProblem
from simpleai.search import beam, breadth_first, astar, greedy, hill_climbing_random_restarts,\
 limited_depth_first, hill_climbing, hill_climbing_stochastic
import sys, getopt


MAX_POINTS = 120
JUMP_FAR = 5
JUMP_CLOSE = 1
COLORFLAT = 1

class SplitImage(object):
    def __init__(self, filepath, max_points, wait):
        self.max_points = max_points
        self.img, readonly = self.load_image(filepath), self.load_image(filepath)
        self.width, self.height = self.img.size
        self.corners = [ (0,0), (self.width, 0), (0, self.height), (self.width, self.height) ]
        self.readpixels = readonly.load()
        self.writepixels = self.img.load()

        self.best = {"value":float("-inf")}
        self.wait = wait

    def pixelize_image(self, method, points=None, outputfile=None):

        if points is None:
            points = [] + self.corners

        my_problem = SplitProblem( (tuple(points), 0), self )

        if method == "astar":
            result = astar(my_problem, graph_search = True)
        elif method == "beam":
            result = beam(my_problem, beam_size = 100)
        elif method == "hill_random":
            result = hill_climbing_random_restarts(my_problem, 2)
        elif method == "hill":
            result = hill_climbing(my_problem)
        else:
            print("Invalid method: {}".format(method))
            return

        print("FINAL RESULT REACHED")
        print("RESULT: {}".format(result.state[0]))
        print("SCORE: {}".format(my_problem.value(result.state)))
        print("PATH: {}".format(result.path()))

        points = result.state[0]
        self.display(points)

        if self.wait:
            a = input("Would you like to improve on this?\n")
            a = a.upper().strip()
            if a not in {"Y","YES","YUP","YEAH"}:
                return

            method_temp = input("Which method? [{}]\n".format(method)).strip().lower()
            if method_temp:
                method = method_temp
            max_points = int(input("How many points? [{}]\n".format(self.max_points)).strip())
            if max_points:
                self.max_points = max_points

            self.pixelize_image(method, points)


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



def main(argv):
    inputfile = "images/andre-sm.png"
    outputfile = None
    wait = False
    method = "hill_random"
    try:
        opts, args = getopt.getopt(argv,"hi:o:n:m:w",["ifile=","ofile=","maxpoints=","method=","wait"])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Will write help soon!')
            sys.exit()
        elif opt in ("-w", "--wait"):
            wait = True
        elif opt in ("-i", "--in"):
            inputfile = arg
        elif opt in ("-m", "--method"):
            method = arg
        elif opt in ("-n", "--maxpoints"):
            max_points = int(arg)
        elif opt in ("-o", "--out"):
            outputfile = arg

    split_image = SplitImage(inputfile, max_points, wait)
    split_image.pixelize_image(method, outputfile = outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])