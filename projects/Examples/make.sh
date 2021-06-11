#!/bin/bash
#
# usage: make.sh	re-build the spec/design/test examples
# 	 make.sh push	push these examples to course website
#
SOURCE_DIR=/home/git/CardFRP
PROSE="overview.html testing.html"
SPECS="gameobject gameaction dice gameactor gamecontext"
SOURCES="base.py gameobject.py gameaction.py dice.py gameactor.py gamecontext.py"

COURSE="cs181aa.f21"
TARGET="markk@knuth.cs.hmc.edu:public_html"

# is this a push
if [ -n "$1" -a "$1" == "push" ]
then
	# generate a list of SPEC files
	SPECFILES=""
	for file in $SPECS
	do
		SPECFILES="$SPECFILES $file-spec.py"
	done
	scp -r $PROSE $SPECFILES $SOURCES html $TARGET/$COURSE/examples
	exit 0
fi
	
echo ... deleting previous example files
if [ -d "html" ]
then
    rm -rf html
fi
for file in $SOURCES $PROSE *-spec.py *.pyc
do
    if [ -f $file ]
    then
	rm -f $file
    fi
done

# were we just cleaning
if [ -n "$1" -a "$1" == "clean" ]
then
	exit 0
fi

echo ... importing prose files
for file in $PROSE
do
	echo "    $file"
	cp $SOURCE_DIR/$file .
done

echo ... importing source files
for file in $SOURCES
do
	echo "    $file"
	python code_strip.py --privates --globals --comments --stop="# UNIT TEST" $SOURCE_DIR/$file $file
done

echo ... creating simpler specification versions
for file in $SPECS
do
	echo "    $file.py -> $file-spec.py"
	python code_strip.py $file.py $file-spec.py
done

echo ... creating class documentation
epydoc -v --graph=umlclasstree $SOURCES
rm *.pyc

