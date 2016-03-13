import json
import os
logs = dict() # image_name => list of entries
num_inserted = dict()

def load_from_file(image_name):
	filepath = get_key(image_name)
	if not os.path.isfile(filepath):
		return []
	else:
		with open(filepath) as fp:
			logs = json.load(fp)["info"]
			return clean_logs(logs)

def clean_logs(logs):
	fn = lambda (state, value) : (len(state[0]), -value)
	logs = sorted(logs, key = fn)
	minimum_value = float("-inf")

	new_logs = list()
	for (state, val) in logs:
		if val >= minimum_value:
			new_logs.append( (state, val) )
			minimum_value = val
	return logs

def load_log(image_name):
	if image_name not in logs:
		val = load_from_file(image_name)
		logs[image_name] = val
	return logs[image_name]

def get_key(image_name):
	return "./out/{}-out.json".format(image_name)

def persist_log(image_name):
	logged = load_log(image_name)
	to_write = {"info" : logged}
	with open(get_key(image_name), "w") as fp:
		json.dump(to_write, fp)

def log(image_name, state, value):
	load_log(image_name).append( (state, value) )
	if image_name not in num_inserted:
		num_inserted[image_name] = 0
	num_inserted[image_name] += 1
	if num_inserted[image_name] >= 20:
		persist_log(image_name)
		num_inserted[image_name] = 0

def best_state(image_name, max_points):
	print("Get best state?")
	logged = load_log(image_name)
	best, best_val = None, float("-inf")
	for state, value in logged:
		points = state[0]
		if value > best_val and len(points) <= max_points:
			best, best_val = state, value
	if best is None:
		return None
	points, time = best
	if points and type(points[0]) is not tuple:
		points = tuple([tuple(a) for a in points])
	print("Got it")
	return points, time
