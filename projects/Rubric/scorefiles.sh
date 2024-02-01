#!/bin/bash
#
# usage: scorefiles.sh project-subdir
#
#   Find the score files in per-team submission directories and
#   make a copy (in a scores directory) for each person in that team.
#   This is useful when we grade a team submission, and want to give
#   a feedback file to each student on the team
#
#   If there are per-student grade files in addition to the per-team
#   grades, those will be appended to the per-student results in the
#   scores directory.
#
#   expectations
#    1.	teams.csv contains lines of the form <team-name>,<student-name>
#    2.	project sub-directory contains a sub-directory for each team
#    3.	team sub-directories contain a files w/name like grading_P1A.txt
#    4. there may also be per-student files (e.g. markk_1D)
#

TEAMFILE=./teams.csv
SCORES=./scores

PROJECT="$1"
if [ -z "$1" -o ! -d "$1" ]
then
    echo "Usage: $0 project-directory" >&2
    exit 1
fi

# make sure we have a clean scores directory
if [ -d $SCORES ]
then
	rm -f $SCORES/*
else
	mkdir $SCORES
fi

# get a list of team directory names
TEAMS=`cat $TEAMFILE | cut -d, -f1 | sort | uniq`

# suffix for per-student score files
SUFFIX="_$PROJECT.txt"

for team in $TEAMS
do
    if [ -d $PROJECT/$team ]
    then
	grade=`echo $PROJECT/$team/grading_*.txt`
	if [ -f $grade ]
	then
	    echo "Team: $team"
	    members=`grep $team $TEAMFILE | cut -d, -f3`
	    for student in $members
	    do
		# create a per-student file with an email address
		email=`grep $student $TEAMFILE | cut -d, -f2`
		echo "EMAIL: $email" > $SCORES/$student$SUFFIX
		echo >> $SCORES/$student$SUFFIX

		# make per-student copy of the team-grade
		cat $grade >> $SCORES/$student$SUFFIX
	    	echo " ... $grade -> $SCORES/$student$SUFFIX"

		# see if there is also a per-student grade
		if [ -f $PROJECT/$team/"$student"_"$PROJECT" ]
		then
		    echo " ...    appending $PROJECT/$team/$student"_"$PROJECT"
		    cat $PROJECT/$team/"$student"_"$PROJECT" >> $SCORES/$student$SUFFIX
		fi
	    done
    	else
	    echo "Unable to find grade sheet in $PROJECT/$team" >&2
	fi
    else
	echo "Unable to find submission directory $PROJECT/$team" >&2
    fi
    echo
done
