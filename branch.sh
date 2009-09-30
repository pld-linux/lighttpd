#!/bin/sh
set -e
svn=svn://svn.lighttpd.net/lighttpd
tag=lighttpd-1.4.23
branch=lighttpd-1.4.x

d=$-
filter() {
	set -$d
	# Excluding files which change version or were not in dist tarball
	filterdiff \
		-x 'ChangeLog' \
		-x 'CMakeLists.txt' \
		-x 'configure.in' \
		-x '.cvsignore' \
		-x 'doc/.cvsignore' \
		-x 'SConstruct' \
		-x 'src/CMakeLists.txt' \
		-x 'src/config.h.cmake' \
		-x 'src/.cvsignore' \
		-x 'src/mod_uploadprogress.c' \
		-x 'tests/.cvsignore' \
		-x 'tests/mod-extforward.conf' \
		-x 'configure.ac' \
		| \
	# remove revno's for smaller diffs
	sed -e 's,^\([-+]\{3\} .*\)\t(revision [0-9]\+)$,\1,'
}

old=$svn/tags/$tag
new=$svn/branches/$branch
echo >&2 "Running diff: $old -> $new"
LC_ALL=C svn diff --old=$old --new=$new | filter > lighttpd-branch.diff.tmp

if cmp -s lighttpd-branch.diff{,.tmp}; then
	echo >&2 "No new diffs..."
	rm -f lighttpd-branch.diff.tmp
	exit 0
fi
mv -f lighttpd-branch.diff{.tmp,}
