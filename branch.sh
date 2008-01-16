#!/bin/sh
svn=svn://svn.lighttpd.net/lighttpd/
tag=lighttpd-1.4.18
branch=lighttpd-1.4.x
svn diff --old=$svn/tags/$tag --new=$svn/branches/$branch > lighttpd-branch.diff
