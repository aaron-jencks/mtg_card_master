from duplicate_copier import *
from mtgsdk import Set
import os, fnmatch, argparse, re

def get_set_id_and_year(file):
    set_code = file.split('_')[0]
    file = remove_ext_and_set(file)
    chunks = file.split('_')
    if chunks[-1].isdigit() and not chunks[-2].isdigit():
        c_id = get_num_id(file)
        is_dated = False
    else:
        c_id = chunks[-2]
        is_dated = True
    release_date = Set.find(set_code).release_date.split('-')[0]
    file = remove_num_id(file)
    return set_code, c_id, release_date, file, is_dated

def create_new_filename(directory, set_code, filename, card_id, year, ext, is_dated):
    os.rename(os.path.join(directory, (set_code + ((filename + str(card_id)) if not is_dated else (filename + str(year))) + ext)), \
                            os.path.join(directory, (set_code + filename + ((str(card_id) + '_') if not is_dated else "") + year + ext)))

if __name__ == "__main__":
	# Documentations and arguments
	parser = argparse.ArgumentParser("Used to copy duplicate cards from one set into another.")
	parser.add_argument("image_dir", help="The set to copy from", type=str)
	parser.add_argument("annotation_dir", help="The set to copy to", type=str)
	args = parser.parse_args()

	if os.path.isdir(args.image_dir) and os.path.isdir(args.annotation_dir):
            for file in fnmatch.filter(os.listdir(args.annotation_dir), "*.xml"):
                print('found source {}'.format(file))
                sc, cid, year, file, is_dated = get_set_id_and_year(file)
                create_new_filename(args.annotation_dir, sc, file, cid, year, ".xml", is_dated)

            for file in fnmatch.filter(os.listdir(args.image_dir), "*.jpg"):
                print('found source {}'.format(file))
                sc, cid, year, file, is_dated = get_set_id_and_year(file)
                create_new_filename(args.image_dir, sc, file, cid, year, ".jpg", is_dated)


