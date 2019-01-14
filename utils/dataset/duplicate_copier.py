from shutil import copyfile
import os
import fnmatch
import argparse

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
		source_files = []
		for file in fnmatch.filter(os.listdir(args.source_dir), args.origin_set + "*.xml"):
			print('found source {}'.format(file))
			# appends the filename, dropping the extension
			source_files.append(os.path.splitext(file)[0][len(args.origin_set):])

		for file in fnmatch.filter(fnmatch.filter(os.listdir(args.target_dir), args.target_set + "*.jpg"), args.pattern):
			# Remove file extension and set name
			file = os.path.splitext(file)[0][len(args.target_set):]
			# Removes the unique identifier
			
			print('Found target file {}'.format(file))

			if file in source_files:
				print('found a match for {}'.format(file))
				copyfile((args.origin_set + file + ".xml"), (args.target_set + file + ".xml"))

