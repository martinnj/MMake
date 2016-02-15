#!/usr/bin/env python3
#
# Copyright (c) 2016 Martin J
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

import argument

def main():
    """
    """

    f = argument.Arguments()
    #Requried arguments, first argument will be stored as "candy"
    f.always("candy", help="Candy name")

    #optional unnamed value
    f.maybe("soda")

    #optional value, set a default, can be changed by adding: --num=30, or -n=30
    f.option("num",
        25,
        help="How many pieces?",
        abbr="n"
        )
    #add a switch, a flag with no argument
    f.switch("reverse",
        help="Reverse ordering",
        abbr="r"
    )
    f.switch("unwrap", help="unwrapcandy", abbr="u")

    #Process data before saving it
    f.process("candy", lambda x: x.upper())
    #Parse num as integer
    f.process("num", lambda x: int(x))
    f.validate("num", lambda x: x > 10)



    #get data
    arguments, errors = f.parse()

    if len(errors) > 0:
        print(errors)
        print
        print(f)
    else:
        print(arguments)

if __name__ == '__main__':
    main()