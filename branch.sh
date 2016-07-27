#!/bin/sh
set -e
svn=svn://svn.lighttpd.net/lighttpd
url=https://git.lighttpd.net/lighttpd/lighttpd1.4.git
package=lighttpd
tag=lighttpd-1.4.40
branch=master
out=$package-branch.diff
repo=$package.git

# old version of this code used to create tarball.
# leave it around
if [ "$1" = "tarball" ]; then
	v=1.5
	svn co $svn/trunk $package-$v
	r=$(svnversion $package-$v)
	t=$package-r$r.tar.bz2
	tar -cjf $t --exclude-vcs $package-$v
	../dropin $t &
	exit 0
fi

d=$-
filter() {
	set -$d
	# Excluding files which change version or were not in dist tarball
	filterdiff \
		-x 'CMakeLists.txt' \
		-x 'configure.ac' \
		-x 'SConstruct' \
	| cat
}

if [ ! -d $repo ]; then
	git clone --bare $url -b $branch $repo
fi

cd $repo
	git fetch
	git diff $tag..$branch | filter > ../$out.tmp
cd ..

if cmp -s $out{,.tmp}; then
	echo >&2 "No new diffs..."
	rm -f $out.tmp
	exit 0
fi
mv -f $out{.tmp,}

../md5 $package.spec
../dropin $out
