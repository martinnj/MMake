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
import re                          # RegExps For parsing the makefile.
import multiprocessing             # For detecting CPU count.
import concurrent.futures          # For thread pool.
from subprocess import Popen, PIPE # For starting external make commands.
import shlex                       # Used to parse argument strings.

# Non standard imports.
import argument           # Provides a parser for arguments.

import depgraph

VERSION = "0.0.1"
VERBOSE = True
SUPRESS = False
WORKERS = 4

def verbose_print(msg):
    """
    Prints the given messag eonly if the global VERBOSE
    variable is set to True.

    @msg a string with the message to print.
    """
    if VERBOSE:
        print(msg)

def yn_prompt(msg):
    """
    Shows a prompt to the user and returns a boolean depending on
    wether the user answered yes or no.

    If the global variable SUPRESS is set, this will always return true.

    @msg the question to ask.
    """

    if SUPRESS:
        return True

    reply = input(msg + "[yn]:")

    while not(reply.strip().lower() == "y" or 
          reply.strip().lower() == "yes" or
          reply.strip().lower() == "n" or 
          reply.strip().lower() == "no"):

        print("Invalid input detected.")
        reply = input(msg + "[yn]:")

    reply = reply.strip().lower()
    if reply == "y" or reply == "yes":
        return True
    else:
        return False

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
        4,
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

    # Supress warnings and take default answers to all questions.
    f.switch("supress",
        help="Supress any questions/warnings, will default to 'yes'.",
        abbr="s"
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

def make_target(makefile, target, args):
    """
    Builds a specific target from a given makefile.

    @makefile path to the makefile we wish to build from.

    @target the target we wish to build.

    @args a string of arguments to pass to the make command.
    """
    cmd = shlex.split("make -f" + makefile + " " + args + " " + target)
    with Popen(cmd, stdout=PIPE) as proc:
        output = proc.stdout.read()
        proc.wait()

        with open(makefile + "." + target + ".log", mode="w") as f:
            f.write(output.decode("utf-8"))
            f.close()

        return proc.returncode
    

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

    global VERBOSE, SUPRESS
    VERBOSE = args["verbose"]
    SUPRESS = args["supress"]

    # Check the thread number.
    if multiprocessing.cpu_count() < args["numthreads"]:
        global WORKERS
        if yn_prompt("The selected number of threads (%d), is larger than " +
                     "the number of cores in your machine (%d), should i " +
                     "decrease it?"):
            WORKERS = multiprocessing.cpu_count()
        else:
            WORKERS = args["numthreads"]


    verbose_print("Verbose output is ON.")
    print("Build Target: " + args["target"])
    print("Processing makefile: " + args["makefile"])
    print("Number of worker threads: " + str(WORKERS))
    print("Arguments that will be passed to each make command:\n\t" +
          str(args["args"] + "\n\n"))

    try:
        with open(args["makefile"]) as f:
            file_content = f.read()
            #for line in content.split('\n'):

            # TODO: Makefile anlysis and dependency graph building.

            makefile_regex = ''
            res = re.search(makefile_regex, file_content)
            f.close()

    except IOError as error:
        print("An error occured while opening the make file:")
        print("    " + str(error))
        exit(1)


    # Creates a threadpool with the required number of threads.
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        print("")
        #Example: https://docs.python.org/dev/library/concurrent.futures.html#threadpoolexecutor-example
        make_target(args["makefile"], args["target"], args["args"])

if __name__ == '__main__':
    main()
