# mtg_card_master

This project is going to be used to identify Magic the gathering cards using tensorflow's object detection api. It will fetch the prices of the cards if it can, and draw relevant information about them on the image as a label on the bounding box.

## Data

In the ./data directory there are a couple of datasets, the bounding_box dataset is used to identify the cards as cards, with no attributes, and the Detail dataset is used to identify attributes of cards (name, CMC, flavor text, artist, etc...).  The text_convertor dataset will be used to convert the text on the card into strings, the icon_identifier will be used to identify sets as strings, and the cost_convertor will be used to identify CMC as strings.

## Models

In each corresponding module's folder, there is a model directory, this contains the model that each module was trained with:

* card_identifier: ssdlite_mobilenet_v2
