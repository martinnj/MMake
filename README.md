# MtMake
MultiThreaded Make wrapper. The idea is to build a dependency graph and
compile the nodes on different threads.

# Requirements
 - Python 3
 - python3-pip
 - [virtualenv](https://pypi.python.org/pypi/virtualenv)
 - [Argument](https://pypi.python.org/pypi/argument)

# Developing
 - ```$ virtualenv -p /usr/bin/python3.4 venv```
 - ```$ source venv/bin/activate```
 - ```$ pip3 install -r requirements.txt```

# License
mtmake is licensed under the MIT license, see the [LICENSE](LICENSE) file for
details.
