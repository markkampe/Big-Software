#!/bin/bash
#
# Process per-user score files and send each, as e-mail, to the associated student.
#
# NOTES:
#
#	score files are assumed:
#		to have names of the form <user>_<project>.txt
#
#	the script tries to identify obviously bogus score files
#	(e.g. that have no total or no known user) and will not
#	try to send messages for them, but it is best to run the
#	script with the "--test" option and clean up any garbage
#	before the final run.
#
USAGE="$0 [--test] score-file ..."

TEAMS=teams.csv

if [ -n "$1" -a "$1" == "--test" ]; then
	let testing=1
	shift
else
	let testing=0
fi

if [ -s "$1" ]; then
	ASSGT=`echo $1 | cut -d_ -f2 | cut -d. -f1`
	echo "Subject: SWE Proejct $ASSGT"
else
	>&2 echo Usage: $USAGE 
	exit 1
fi

let errors=0
# sendMail address assignment scorefile total
function sendMail {
	ats=`echo $1 | grep '@' | wc -l`
	if [ $ats -eq 1 ]; then
		echo -e -n "   $3 ($4) \t -> $1, subject=$2  ... " 
		if [ $testing -eq 0 ]; then
			mutt -s "SWE $2" $1 < $3
			ret=$?
			if [ $ret -eq 0 ]; then
				echo "OK"
			else
				echo "mutt returns $ret"
			fi
		else
			echo "READY"
		fi
	else
		>& 2 echo "ERROR - $3: INVALID EMAIL ADDRESS ($1)"
		let errors+=1
	fi
}

# iterate through all specified files
while [ -n "$1" ]; do
	if [ ! -s $1 ]; then
		echo "    $1 ... UNABLE TO OPEN"
		let errors+=1
	else 
		# some people edit their files on Windows!!!
		tr '\r' '\n' < $1 > /tmp/$$

		# pull some interesting information out of the assignment
		USER=`echo $1 | cut -d_ -f1 | cut -d/ -f2`
		EMAIL=`grep $USER $TEAMS | cut -d, -f2`
		TOTAL=`grep "Total Score:" /tmp/$$ | cut -s -d: -f2 | tr -d \[:blank:\]`

		if [ -z "$EMAIL" ]; then
			>& 2 echo "ERROR - $1: CONTAINS NO EMAIL ADDRESS"
			let errors+=1
		elif [ -z "$TOTAL" ]; then
			>& 2 echo "ERROR - $1: CONTAINS NO TOTAL SCORE"
			let errors+=1
		else
			sendMail $EMAIL "$ASSGT" $1 $TOTAL
		fi

		rm -f /tmp/$$
	fi
	shift
done

if [ $errors -eq 0 ]; then
	exit 0
else
	exit 1
fi
