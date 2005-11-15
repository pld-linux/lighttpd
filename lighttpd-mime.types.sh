#!/bin/sh
# Parse /etc/mime.types into lighttpd config format.
# Copyright (c) 2005 Elan Ruusamäe <glen@pld-linux.org>

mimetypes="$1"

# build mime.types from system mime.types
# get ones with extension
awk '!/^#/ && $2 { print } ' $mimetypes | \
# lay out mime types with multiple extension as separate lines \
awk '{for (a=2; a <= NF; a++) {printf("%s\t%s\n", $1, $a)}}' | \
# sort it \
LC_ALL=C sort -u > mime.types

# build lighttpd.conf fragment
awk '{ printf("\t\".%s\"%s=> \"%s\",\n", $2, (length($2) > 4 ? "\t" : "\t\t"), $1)}' \
	< mime.types | LC_ALL=C sort -r > mime.types.conf

# sanity check. there can't be more than one mime type mapping for same extension
dup=$(awk -F'"' '{print $2}' mime.types.conf | sort | uniq -c | grep -v '1' | awk '{print $NF}')
if [ "$dup" ]; then
	echo >&2 Found $(echo "$dup" | wc -w) extensions which have non-unique mime-type mapping:
	echo "$dup" | sed -e 's,^,  ,' >&2
	exit 1
fi

mv -f mime.types.conf mime.types.conf.tmp

# header
cat >> mime.types.conf <<EOF
# mimetype mapping
mimetype.assign = (
EOF

# save our hard work
cat mime.types.conf.tmp >> mime.types.conf

# footer
cat >> mime.types.conf <<EOF
)
EOF
