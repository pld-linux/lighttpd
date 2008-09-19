#!/bin/sh
set -e
svn=svn://svn.lighttpd.net/lighttpd
tag=lighttpd-1.4.19
branch=lighttpd-1.4.x

old=$svn/tags/$tag
new=$svn/branches/$branch
echo "Running diff: $old -> $new"
LC_ALL=C svn diff --old=$old --new=$new > lighttpd-branch.diff

echo "Excluding files which change version or were not in dist tarball"
filterdiff -x 'configure.in' -x .cvsignore lighttpd-branch.diff > lighttpd-branch.diff.tmp
mv -f lighttpd-branch.diff.tmp lighttpd-branch.diff