#!/bin/bash

# Usage: ./create_mass_annotation.sh ./annotations/lsdkfjlsdjf.xml ./images/*.jpg
# Copies the annotation and renames it to each jpg file in the images folder

files=$(find "$2" -type f -maxdepth 1 -name "$3")
total=$(ls -1 ${files} | wc -l)
echo "Found ${total} files to convert"
for filename in ${files}; do
	[ -e "$filename" ] || continue
	echo "Converting ${filename}"
	cp "${1}" "$(dirname "${1}")/$(basename "${filename}" ".jpg").xml"
done
