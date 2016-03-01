

# Splitter

This let's you split an image into low-res triangles. It uses some basic AI tools to break up the image in the most optimal places so that we reproduce the original image as best as possible. It tries to minimize the average color "distance" between the actual color of a pixel and the color of the triangle that covers it. Less difference is better. 

## Examples

Most of these use the `simpleai` library's local search functions to find a near optimal solution. However, the solutions aren't really that good yet.

![Alt text](/images/panda-sm.png "Panda plain")
![Alt text](/out/panda-out-1.png "Panda low")
![Alt text](/out/panda-out.png "Panda highres")

![Alt text](/images/andre-sm.png "Aghassi normie")
![Alt text](/out/andre-out.png "Aghassi post aesthetics")

## Usage

Use `python main.py` with the following command line uptions:

* `-i`, `--infile` : The filepath to the input image
* `-o`, `--outfile` : The filepath to the output image. Not yet implemented.
* `-m`, `--method` : The search method to use to find a solution. The default is hill climbing with random seeding. The following methods are implemented:
	* `astar` : astar search
	* `beam` : beam search
	* `hill_random` : hill climbing with random seeding
	* `hill` : hill climbing
* `-w`, `--wait` : After processing the image, it will give you the chance to run further improvements on it and adjust settings.
* `-n`, `--maxpoints` : The maximum amount of polygon points to allow the algorithm.

So here's an example:

`python main.py -i images/panda-sm.png -w -n 8 -m hill_random`