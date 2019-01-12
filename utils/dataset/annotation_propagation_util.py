from shutil import copyfile
import argparse
import os
import sys
import fnmatch

"""I used this program to copy an annotation xml file and rename it to every card in a set
with given characteristics, helps for doing annotations for different card layouts and types
for example:
copy some creature card from 10th edition to every creature card in 10th edition, so I don't
have to do their annotations
copy some instant card from 10th edition to every instant card in 10th edition.

The images are named such that you can do this with simple pattern matching.
"""

parser = argparse.ArgumentParser("Searches for any file matching the pattern and then copies it to contain the contents in the target.")
parser.add_argument("target_file", help="The file to whom's contents to copy", type=str)
parser.add_argument("pattern_dir", help="The directory to search for pattern matches in", type=str)
parser.add_argument("pattern", help="The fnmatch pattern to use", type=str)
args = parser.parse_args()

if __name__ == "__main__":
	print('Finding matches")
	files = []
	for f in os.listdir(args.pattern_dir):
		if fnmatch.fnmatch(f, args.pattern):
			print('Located copying target ' + f)
			files.append(f)
	print('Copying files')
	# Extracts the extension from the filename
	_, ext = os.path.splitext(target_file)
	output_path, _ = os.path.split(target_file)
	for f in files:
		name, _ = os.path.splitext(os.path.basename(f))
		new_file = os.path.join(output_path, name + ext)
		print('Copying to ' + new_file)
		copyfile(args.target_file, new_file)
