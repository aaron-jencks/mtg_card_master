from mtgsdk import Card, Set
from random import shuffle, choices
import urllib.request as url
import argparse, os

parser = argparse.ArgumentParser()
parser.add_argument('output_path', help="Directory to store the image files into.", type=str, default="./")
args = parser.parse_args()

def card_to_filename(card) -> str:
	"""Takes a mtgsdk Card object and returns a filename
	containing the types and formats, border styles, etc..."""
	result = card.set + "_" + card.name.replace(' ', '_') + "_"
	result += card.type.split()[0] + "_"
	result += card.border + "_" if card.border else ""
	result += str(card.multiverse_id)
	return result

def collect_card_dict():
    """Creates a dictionary of cards
    where each key is a set name"""
    result = {}
    for card_set in Set.all():
	    if not card_set.online_only:
		    print('Retrieving ' + card_set.name + ' aka ' + card_set.code)
		    cards = Card.where(set=card_set.code).all()
		    result[card_set.code] = cards
    return result

def add_to_dict_list_or_create(list_dict, key, item):
	"""Adds an item to a list in a dictionary or
	creates an empty list and inserts it first"""

	if key in list_dict:
		list_dict[key].append(item)
	else:
		list_dict[key] = [item]

def create_type_dict_from_set(card_list):
	"""Takes a set of cards, splits it into
	the visually different groups"""

	type_dict = {}
	for card in card_list:
		#print('Sorting ' + card.name)
		if len(card.colors) > 1:
			# If the card is multi-colored we'll put it into a separate sections
			add_to_dict_list_or_create(type_dict, "MultiColor", card)
			continue
		types = card.type.split()
		if types[0] is not "Basic":
			if types[0] is "Artifact" and len(types) > 1 and types[1] is "Creature":
				# Balances the Artifact Creatures between the two categories
				if "Artifact" in type_dict and not "Creature" in type_dict:
					add_to_dict_list_or_create(type_dict, "Creature", card)
				elif "Creature" in type_dict and not "Artifact" in type_dict:
					add_to_dict_list_or_create(type_dict, "Artifact", card)
				elif len(type_dict["Artifact"]) > len(type_dict["Creature"]):
					type_dict["Creature"].append(card)
				else:
					type_dict["Artifact"].append(card)
			else:
				# Add the card to the dictionary as usual
				add_to_dict_list_or_create(type_dict, types[0], card)
		elif types[0] is "Instant" or types[0] is "Sorcery" or types[0] is "Enchantment":
			# Enchantments, Instants, and Sorceries all have the same basic layout
			add_to_dict_list_or_create(type_dict, "Spell", card)
		else:
			# The card is a basic land, sort by type not land
			# Mountain, Forest, Island, etc...
			add_to_dict_list_or_create(type_dict, types[3], card)
			
	return type_dict
	
def filter_set(card_set):
    """Cuts a card_set in half 
    equally balancing all visually
    different card types"""
    
    compendium = []
    type_dict = create_type_dict_from_set(card_set)
    for card_type in type_dict:
        for card in choices(type_dict[card_type], k=int(len(type_dict[card_type]) / 2)):
            compendium.append(card)
            
    return compendium
				

if __name__ == "__main__":
    print('Collecting cards, this may take some time')
    card_dict = collect_card_dict()
    
    for card_set in card_dict:
        print('Sorting ' + card_set)
        chosen_cards = filter_set(card_dict[card_set])
        print('Collecting images')
        for card in chosen_cards:
            try:
                print('Downloading ' + card.name + ' from ' + card.image_url)
                url.urlretrieve(card.image_url, os.path.join(args.output_path, card_to_filename(card) + ".jpg"))
            except:
                print('skipping ' + card.name + ' url property is empty')
