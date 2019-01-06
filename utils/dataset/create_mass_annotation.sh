#!/bin/bash

# Usage: ./create_mass_annotation.sh ./annotations/lsdkfjlsdjf.xml ./images/*.jpg
# Copies the annotation and renames it to each jpg file in the images folder

total=$(ls -1 $2 | wc -l)
echo "Found ${total} files to convert"
for filename in $2; do
	[ -e "$filename" ] || continue
	echo "Converting ${filename}"
	cp "${1}" "$(dirname "${1}")/$(basename "${filename}" ".jpg").xml"
done
