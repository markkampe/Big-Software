INTERMEDIATES=proj_1.h proj_2.h proj_3.h proj_4.h grading.h
DOC_HTML="<head\|<HEAD\|<body\|<BODY\|<html\|<HTML\|</HEAD\|</body\|</BODY\|</html\|</HTML\|<title\|<TITLE"
INCLUDES=/home/git/CourseWare/Website

SCHOOL=HMC
COURSE=SWE
MONTH=9
YEAR=2020

projects.html: projects.c $(INTERMEDIATES)
	gcc -I$(INCLUDES) -E -DSWE -DYEAR=$(YEAR) -DMONTH=$(MONTH) -D$(SCHOOL) -w projects.c | grep -v '^# ' > $@
	rm $(INTERMEDIATES)

%.h : %.html
	grep -v $(DOC_HTML) $< > $@

clean:
	rm -f $(INTERMEDIATES) projects.html
