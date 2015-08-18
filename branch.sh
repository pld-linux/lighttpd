#!/bin/sh
set -e
svn=svn://svn.lighttpd.net/lighttpd
package=lighttpd
tag=lighttpd-1.4.36
branch=lighttpd-1.4.x
out=lighttpd-branch.diff

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
		| \
	# remove revno's for smaller diffs
	sed -e 's,^\([-+]\{3\} .*\)\t(revision [0-9]\+)$,\1,'
}

old=$svn/tags/$tag
new=$svn/branches/$branch
echo >&2 "Running diff: $old -> $new"
LC_ALL=C svn diff --old=$old --new=$new > $out.tmp
revno=$(sed -ne 's,^[-+]\{3\} .*\t(revision \([0-9]\+\))$,\1,p' $out.tmp | sort -urn | head -n1)
echo >&2 "Revision $revno"
[ "$revno" -gt 0 ] || exit 1

sed -i -e "1i# Revision $revno" $out.tmp
filter < $out.tmp > $out.tmp2 && mv -f $out.{tmp2,tmp}

if cmp -s $out{,.tmp}; then
	echo >&2 "No new diffs..."
	rm -f $out.tmp
	exit 0
fi
mv -f $out{.tmp,}

../md5 *.spec
