
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
    make_gallery = False

    try:
        opts, args = getopt.getopt(argv,"hi:o:n:m:wpg",["ifile=","ofile=","maxpoints=","method=","wait","profile","gallery"])
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
        elif opt in ("-g", "--gallery"):
            make_gallery = True
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
    if make_gallery:
        split_image.make_gallery()
    else:
        split_image.pixelize_image(method)

    if profile:
        pr.disable()
        pr.print_stats()

if __name__ == "__main__":
    main(sys.argv[1:])