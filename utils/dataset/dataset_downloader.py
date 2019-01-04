#!/bin/python3

import mtgsdk as mtg
from mtgsdk import *
import numpy as np
import cv2
import argparse
import urllib

# Documentation
parser = argparse.ArgumentParser("Used to download and convert images using mtg's sdk and convert them into images and annotations")
parser.add_argument('-s', '--set', help="Used to determine which set to download, by default is 'all'", type=str, default="all")
parser.add_argument('-a', '--all', help="Overrides all other arguments, and downloads every card ever made", action="store_true")
parser.add_argument('output_dir', help="Output directory for the annotations and image files, will be put into their respective own subdirectory", type=str, default=".")
args = parser.pars_args()

def card_to_xml(card):
	"""Converts any given mtgsdk card class into
	into a tf xml annotation"""
	pass

if __name__ == "__main__":
	import sys

	# This will be used to download images using mtg's sdk
	# You can pass in any number of arguments

	cards = []
	if args.all or args.set is "all":
		print('Downloading all cards ever printed, may take some time')
		cards = Card.all()
	else:
		print('Downloading cards from ' + args.set + ' set')
		cards = Cars.where(set=args.set).all()

	for card in cards:
		urllib.urlretrieve(card.image_url, 
