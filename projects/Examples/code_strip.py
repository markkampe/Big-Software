#!/usr/bin/python
#
# simple program to copy one file to another up until some stop marker
#   I use it to strip testing code out of sample programs
#
# usage: python copy.py --stop="some string" infile outfile
#
import sys


def copy_file(source, dest, opts):

    in_file = open(source, "rb")
    out_file = open(dest, "w")
    stop_at = opts.stop_string
    lose = opts.strip_string
    show_globals = opts.globals

    lines = 0           # lines copied this far
    blanklines = 0      # no buffered up blank lines
    stopped = False     # we have not hit the stop string
    name = None         # we are in no method or class
    private = False     # we are not in a private method
    docstring = False   # we are no in a docstring
    definition = False  # we are not in the middle of def/class parms

    for line in in_file:
        # we want to look at the first real token
        stuff = line.strip()

        # see if we have hit the stop string
        if stop_at is not None and stuff.startswith(stop_at):
            stopped = True
            break

        # see if this is a line we are suppsed to ignore
        if lose is not None and stuff.startswith(lose):
            continue

        # see if we are defining a method
        if stuff:
            words = stuff.split()
            if words[0] == "def" or words[0] == "class":
                name = words[1].split("(")[0]
                private = name.startswith("_")
                if opts.verbose:
                    print("   ... found " +
                          ("private" if private else "public") +
                          (" method " if words[0] == "def" else " class ") +
                          name)

                # if we will copy this def/class, copy preceeding blanks
                if opts.privates or not private:
                    for _ in range(blanklines):
                        out_file.write("\n")
                    blanklines = 0
                    definition = True

        # print out defs until we finish the parameters
        if definition:
            out_file.write(line)
            lines += 1
            if ")" in stuff:
                definition = False
            continue

        # accumulate successive blank lines after a method
        if name is not None:
            if not stuff and not docstring:
                blanklines += 1
                continue
            else:
                blanklines = 0

        # are we skipping private methods entirely
        if private and not opts.privates:
            continue

        # are we skipping code comments
        comment = stuff.startswith("#")
        if comment and name is not None and not opts.comments:
            continue

        # figure out if we are in a docstring
        if '"""' in stuff:
            # is it a one liner, or multi-line
            instances = 0
            for substr in stuff.split():
                if substr == '"""':
                    instances += 1
            if instances == 1:
                docstring = not docstring
        elif not comment and not docstring:
            # only comments docstrings and globals get through
            if name is not None or not show_globals:
                continue

        # pass this line through
        out_file.write(line)
        lines += 1

    in_file.close()
    out_file.close()
    result = "copied " + str(lines) + " lines from " + source + \
             " to " + dest
    if stopped:
        result += ", before '" + opts.stop_string + "'"
    return result


if __name__ == '__main__':
    from optparse import OptionParser

    umsg = "Usage: %prog [options] input_file output_file"
    parser = OptionParser(usage=umsg)
    parser.add_option("-s", "--stop", type="string",
                      dest="stop_string", metavar="STRING", default=None,
                      help="stop copy at this line")
    parser.add_option("-p", "--privates", action="store_true", dest="privates",
                      help="include private methods")
    parser.add_option("-g", "--globals", action="store_true", dest="globals",
                      help="include global variables and code")
    parser.add_option("-c", "--comments", action="store_true", dest="comments",
                      help="include in-method comments")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      help="verbose output")
    parser.add_option("-x", "--strip", type="string",
                      dest="strip_string", metavar="STRING", default="# pylint:",
                      help="strip lines that begin with")

    (opts, files) = parser.parse_args()

    if len(files) != 2:
        sys.stderr.write(umsg)
    else:
        result = copy_file(files[0], files[1], opts)
        print("   ... " + result)
