#!/bin/sh
set -e
svn=svn://svn.lighttpd.net/lighttpd
tag=lighttpd-1.4.18
branch=lighttpd-1.4.x

old=$svn/tags/$tag
new=$svn/branches/$branch
echo "Running diff: $old -> $new"
LC_ALL=C svn diff --old=$old --new=$new > lighttpd-branch.diff

echo "exclude files which change version"
filterdiff -x 'configure.in' -x 'SConstruct' lighttpd-branch.diff > lighttpd-branch.diff.tmp
mv -f lighttpd-branch.diff.tmp lighttpd-branch.diff
