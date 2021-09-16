#!/bin/bash
#
#   run this script in a new Grading directory to set it up for
#   use by the standard SWE grading script tools
#
SOURCE="/home/git/Big-Software/projects/Rubric"
CONFIG="/home/markk/Dropbox/Shuttle"
if [ -d "/home/git/Toys" ]
then
    TOYS="/home/git/Toys/bash"
else
    TOYS="/home/git/toys/bash"
fi

# most good stuff comes from here
ln -s $SOURCE .

# symlinks to scripts
ln -s $SOURCE/perteam.sh .
ln -s $SOURCE/peruser.sh .
ln -s $SOURCE/scorefiles.sh .
ln -s $TOYS/x2pdf.sh .

# data/configuration files
ln -s $CONFIG/slip_days .
ln -s $CONFIG/teams.csv .

# needed directories
if [ ! -d scores ]
then
    mkdir scores
fi
