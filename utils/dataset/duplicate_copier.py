from shutil import copyfile
import os
import fnmatch
import argparse
import re

exp_set = re.compile(r'^[0-9a-zA-Z]+')
def remove_ext_and_set(filename):
	"""Removes the file extension and the magic set
	number from the given filename"""

	global exp_set

	m = exp_set.search(filename)

	if m:
		return os.path.splitext( filename)[0][m.end():]
	else:
		return os.path.splitext(filename)[0]

# The next two methods use this
exp = re.compile(r"\d+$")

def get_num_id(filename):
	"""Returns the numeric id number from a card filename"""

	global exp

	m = exp.search(filename)

	return m.group() if m else None

def remove_num_id(filename):
	"""Removes the numeric id number from a card filename"""

	global exp

	m = exp.search(filename)
	if m:
		filename = filename[:m.start()]
	return filename

if __name__ == "__main__":
	# Documentations and arguments
	parser = argparse.ArgumentParser("Used to copy duplicate cards from one set into another.")
	parser.add_argument("origin_set", help="The set to copy from", type=str)
	parser.add_argument("target_set", help="The set to copy to", type=str)
	parser.add_argument("-p", "--pattern", help="The pattern to use when searching for matches in the target", type=str, default="*")
	parser.add_argument("-s", "--source_dir", help="The directory to get the annotations from", type=str, default="./annotations")
	parser.add_argument("-t", "--target_dir", help="The directory to get the matches from", type=str, default="./images")
	args = parser.parse_args()

	if os.path.isdir(args.source_dir) and os.path.isdir(args.target_dir):
		sid_dict = {}
		source_files = []
		for file in fnmatch.filter(os.listdir(args.source_dir), args.origin_set + "*.xml"):
			print('found source {}'.format(file))
			file = remove_ext_and_set(file)
			c_id = get_num_id(file)
			# appends the filename, dropping the extension, saves the id for later
			file = remove_num_id(file)
			source_files.append(file)
			sid_dict[file] = c_id

		tid_dict = {}

		for file in fnmatch.filter(fnmatch.filter(os.listdir(args.target_dir), args.target_set + "*.jpg"), args.pattern):
			file = remove_ext_and_set(file)
			c_id = get_num_id(file)
			# Remove file extension and set name, saves the id for later
			file = remove_num_id(file)
			tid_dict[file] = c_id

			print('Found target file {}'.format(file))

			if file in source_files:
				print('found a match for {}'.format(file))
				copyfile(os.path.join(args.source_dir, (args.origin_set + file + sid_dict[file] + ".xml")), \
					os.path.join(args.source_dir, (args.target_set + file + tid_dict[file] + ".xml")))

