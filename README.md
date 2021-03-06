# MtMake [![Build Status](https://travis-ci.org/martinnj/mtmake.svg?branch=master)](https://travis-ci.org/martinnj/mtmake)
MultiThreaded Make wrapper. The idea is to build a dependency graph and
compile the nodes on different threads.

# Requirements
 - Python 3.4 - 3.5
 - [pip](https://pypi.python.org/pypi/pip)
 - [virtualenv](https://pypi.python.org/pypi/virtualenv)
 - [argument](https://pypi.python.org/pypi/argument)
 - [nose](https://pypi.python.org/pypi/nose)

# Setting up the development environment on Linux

The commands for your package manager might be different from mine. But this
should work on Mint, Debian and Ubuntu.

 - ```# apt-get install python3 python3-pip```
 - ```# pip3 install virtualenv```
 - ```$ git clone git@github.com:martinnj/mtmake```
 - ```$ cd mtmake```
 - ```$ virtualenv -p /usr/bin/python3.4 venv``` (you can substitute which ever
   version of Python 3, but I use 3.4)
 - ```$ source venv/bin/activate```
 - ```$ pip3 install -r requirements.txt```
 - Do development!
 - ```$ deactivate```

# License
mtmake is licensed under the MIT license, see the [LICENSE](LICENSE) file for
details.
