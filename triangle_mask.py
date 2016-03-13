import util

def replace_triangle_point(self, triangle, old_point, new_point):
	return tuple( [point if point != old_point else new_point for point in triangle] )

class TriangleMask(object):
	"""docstring for TriangleMask"""
	def __init__(self, width, height, triangles=None, points=None):
		
		if points is None:
			points = self.generate_corners(width, height)
		
		if triangles is None:
			triangles = util.triangularize_points(points)
		triangles = [sorted(tri) for tri in triangles]

		self.triangles = triangles
		self.points = points
		self.width = width
		self.height = height

	def generate_corners(self, width, height):
		return tuple([ (0, 0), (0, width), (height, 0), (height, width)])

	def move_point(self, old_point, new_point):
		# TODO: What if this causes triangles to intersect?
		replace_point = lambda point: point if point != old_point else new_point
		replace_triangle = lambda triangle: map(triangle, replace_point)

		new_triangles = map(self.triangles, replace_triangle)
		new_point = map(self.point, replace_point)

		return TriangleMask(self.width, self.height, new_triangles, new_points)





		
		