#!/bin/sh
set -e
svn=svn://svn.lighttpd.net/lighttpd
p=lighttpd
v=1.5

svn co $svn/trunk $p-$v
r=$(svnversion $p-$v)
t=$p-r$r.tar.bz2
tar -cjf $t --exclude-vcs $p-$v
../dropin $t &
