#!/bin/bash
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

if [ ! $# -gt 1 ]; then
	echo 1>&2 Usage: fixperms.sh VIRUTAL_ENV ENV_VARS ...
	exit 1
fi

VIRUTAL_DIR=$1
PREFIX=`pwd`

# Set environment variables
shift
for V in "$@"
do
	name=${V%%=*}
	value=${V#*=}
	export $name="$value"
done

chmod a+w $PREFIX/tmp 2>/dev/null
chmod g+s $PREFIX/tmp 2>/dev/null
chmod a+w $PREFIX/logs 2>/dev/null
chmod g+s $PREFIX/logs 2>/dev/null
chmod a+w $PREFIX/import/spacetelescope.org/images 2>/dev/null
chmod g+s $PREFIX/import/spacetelescope.org/images 2>/dev/null
chmod a+w $PREFIX/import/spacetelescope.org/images/processing 2>/dev/null
chmod g+s $PREFIX/import/spacetelescope.org/images/processing 2>/dev/null
chmod a+w $PREFIX/docs/static/images 2>/dev/null
chmod g+s $PREFIX/docs/static/images 2>/dev/null
chmod a+w $PREFIX/docs/static/videos 2>/dev/null
chmod g+s $PREFIX/docs/static/videos 2>/dev/null
chmod a+w $PREFIX/docs/static/releases 2>/dev/null
chmod g+s $PREFIX/docs/static/releases 2>/dev/null
chmod a+w $PREFIX/docs/static/css 2>/dev/null
chmod g+s $PREFIX/docs/static/css 2>/dev/null
chmod a+w $PREFIX/docs/static/js 2>/dev/null
chmod g+s $PREFIX/docs/static/js 2>/dev/null

exit 0