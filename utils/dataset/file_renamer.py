import os
import argparse
import fnmatch

def remove_invalid_chars(string):
	"""Removes the characters in the filename that aren't
	allowed in windows (?,."'\, etc...)"""

	string.replace('<', '_')
	string.replace('>', '_')
	string.replace(':', '_')
	string.replace('"', '_')
	string.replace('/', '_')
	string.replace('\\', '_')
	string.replace('|', '_')
	string.replace('?', '_')
	string.replace('*', '_')

	return string


def contains_invalid_chars(string):
	"""Returns true if the given string contains
	invalid filename characters"""

	return ('<' in string) or ('>' in string) or (':' in string) or ('"' in string) or \
		('/' in string) or ('\\' in string) or ('|' in string) or ('?' in string) or \
		('*' in string)

if __name__ == "__main__":
	parser = argparse.ArgumentParser("Renames files to contain only valid filename characters")
	parser.add_argument("input_dir", help="The directory to perform the operation on", type=str, default=".")
	parser.add_argument("-p", "--pattern", help="The pattern to use to match file names", type=str, default="*")
	args = parser.parse_args()

	for filename in fnmatch.filter(os.listdir(args.input_dir), args.pattern):
		if contains_invalid_chars(filename):
			print('Removing invalid chars from {}'.format(filename))
			os.rename(os.path.join(args.input_dir, filename), os.path.join(args.input_dir, remove_invalid_chars(filename)))
