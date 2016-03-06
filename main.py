
import sys, getopt
import cProfile, pstats
from split_image import SplitImage


def main(argv):
    inputfile = "images/andre-sm.png"
    outputfile = None
    wait = False
    method = "hill_random"
    max_points = 5
    profile = False

    try:
        opts, args = getopt.getopt(argv,"hi:o:n:m:wp",["ifile=","ofile=","maxpoints=","method=","wait","profile"])
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
        elif opt in ("-p", "--profile"):
            profile = True

    if profile:
        pr = cProfile.Profile()
        pr.enable()


    shrink_factor = 1
    split_image = SplitImage(inputfile, max_points, wait, shrink_factor)
    split_image.pixelize_image(method, outputfile = outputfile)

    if profile:
        pr.disable()
        pr.print_stats()


if __name__ == "__main__":
    main(sys.argv[1:])