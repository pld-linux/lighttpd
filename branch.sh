#!/bin/sh
set -e
svn=svn://svn.lighttpd.net/lighttpd
tag=lighttpd-1.4.23
branch=lighttpd-1.4.x

old=$svn/tags/$tag
new=$svn/branches/$branch
echo "Running diff: $old -> $new"
LC_ALL=C svn diff --old=$old --new=$new > lighttpd-branch.diff.tmp

echo "Excluding files which change version or were not in dist tarball"
filterdiff -x tests/mod-extforward.conf -x ChangeLog -x .cvsignore -x src/.cvsignore -x tests/.cvsignore -x doc/.cvsignore -x 'configure.in' -x 'SConstruct' -x 'CMakeLists.txt' -x 'src/CMakeLists.txt' -x 'src/config.h.cmake' -x 'src/mod_uploadprogress.c' lighttpd-branch.diff.tmp > lighttpd-branch.diff.tmp2
mv -f lighttpd-branch.diff.tmp2 lighttpd-branch.diff
rm -f lighttpd-branch.diff.tmp

# remove revno's for smaller diffs
sed -i -e 's,^\([-+]\{3\} .*\)\t(revision [0-9]\+)$,\1,' lighttpd-branch.diff
