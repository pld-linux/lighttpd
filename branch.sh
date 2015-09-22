#!/bin/sh
set -e
svn=svn://svn.lighttpd.net/lighttpd
package=lighttpd
tag=lighttpd-1.4.36
branch=lighttpd-1.4.x
out=lighttpd-branch.diff

v=1.5
# last rev of 1.5 before it's moved to "dead" branch
rev=3039

svn co $svn/trunk${rev:+@$rev} $package-$v
r=$(svnversion $package-$v)
t=$package-r$r.tar.bz2
tar -cjf $t --exclude-vcs $package-$v
../dropin $t &
