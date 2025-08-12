Data (in ~/WIP)
 - teams.csv			... <team,email,user> list
 - slip_days			... user, days used, where

Scripts
 - setup.sh			... create a new to level grading directory
 - perteam.sh project rubric	... create project and team grading directories/files
 - peruser.sh project rubric	... create supplmentary per-user grade files
 				    (ONLY if there are individual submissions)
 - scorefiles.sh project	... create per-user project score reports
 - grademail.sh [--test] scorefiles	... generate email for all scores

 - x2pdf.sh inputfile student	... turn a student-submitted .txt into a .pdf
			            (for uploading exams to gradescope)
Sample usage:
	
	# create and initialize course grading directory
	mkdir ~/Grading
	cd ~/Grading
	/home/git/Big-Software/projects/rubric/setup.sh
	
	# create and initialize project 3A grading directory
	./perteam.sh P2A Rubric/rubric_3a_team.txt
	./peruser.sh P2A Rubric/rubric_3a.txt

	# after editing the per-team and individual rubric files
	./scorefiles.sh P3A
	grep Total scores/*_P3A.txt
	./grademail.sh --test scores/*_P3A.txt

	# and if all looks good, again with out the --test
	
Sub-directories
 - scores			... ready-to-upload score sheets
 - P*/team			... project grading sub-directories
 				    containing both submissions and per team/user grade files

