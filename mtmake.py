#!/usr/bin/env python3
#
# Copyright (c) 2016 Sarah V. Nøhr & Martin J
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



#Makefile structure:
#
#rulename <colon> <space seperated dependency list>
#<tab> <command>

# Standard imports.

import re                 # RegExps For parsing the makefile.
import multiprocessing    # For detecting CPU count.
import concurrent.futures # For thread pool.

# Non standard imports.
import argument           # Provides a parser for arguments.

VERSION = "0.0.1"
VERBOSE = True

def verbose_print(msg):
    """
    Prints the given messag eonly if the global VERBOSE
    variable is set to True.

    @msg a string with the message to print.
    """
    if VERBOSE:
        print(msg)

def create_arguments():
    """
    Create the argument parser instance the program uses.
    """
    f = argument.Arguments()

    # The Makefile to build from.
    f.option("makefile",
        "Makefile",
        help="The makefile to build from.",
        abbr="f"
        )
    f.validate("makefile", lambda x: len(x) >= 1)

    # Number of threads to use for building.
    f.option("numthreads",
        2,
        help="Number of worker threads.",
        abbr="n"
        )
    f.process("numthreads", lambda x: int(x))
    f.validate("numthreads", lambda x: x >= 1)

    # The build target to attempt to build.
    # TODO: Is there any limitations to the targetnames?
    f.option("target",
        "all",
        help="The target to build.",
        abbr="t"
        )
    f.validate("target", lambda x: len(x) >= 2)

    # arguments we do not use but pass on to the make commands.
    f.option("args",
        "",
        help="String with arguments to pass through to the make commands.",
        abbr="a"
        )

    # Display verbose output or normal.
    f.switch("verbose",
        help="Display verbose output while running.",
        abbr="v"
        )

    # Simply display the help.
    f.switch("help",
        help="Displays the usage information/help.",
        abbr="h"
        )
    return f

def print_help(args_parser):
    """
    Prints the help tips from a argument parsers and exits.

    @args_parser argument parser to print before exit.
    """
    print(args_parser)
    exit(1)

def print_greeter():
    """
    Prints a simple welcome message.
    """
    print(" MtMake version " + VERSION)
    print(" Copyright (c) 2016 Sarah V. Nøhr & Martin J\n\n")

def make_target(makefile, target):
    """
    Builds a specific target from a given makefile.

    @makefile path to the makefile we wish to build from.

    @target the target we wish to build.
    """

def main():

    print_greeter()

    args_parser = create_arguments()

    args, errors = args_parser.parse()
    
    if len(errors) > 0:
        print("The following errors was found with the arguments:")
        for error in errors:
            print(error)
        print("")
        print_help(args_parser)


    if args["help"]:
        print_help(args_parser)

    print
    print("Build Target: " + str(args["target"]))
    print("Processing makefile: " + str(args["makefile"]))
    print("Number of worker threads: " + str(args["numthreads"]))
    print("Arguments that will be passed to each make command:\n\t" + str(args["args"] + "\n\n"))

    try:
        with open(args["makefile"]) as f:
            file_content = f.read()
            #for line in content.split('\n'):

            # TODO: Makefile anlysis and dependency graph building.

            makefile_regex = '[]'
            res = re.search(makefile_regex, file_content)
            f.close()

    except IOError as error:
        print("An error occured while opening the make file:")
        print("    " + str(error))
        exit(1)


    # Creates a threadpool with the required number of threads.
    with concurrent.futures.ThreadPoolExecutor(max_workers=args["numthreads"]) as executor:
        print("")
        #Example: https://docs.python.org/dev/library/concurrent.futures.html#threadpoolexecutor-example

if __name__ == '__main__':
    main()
