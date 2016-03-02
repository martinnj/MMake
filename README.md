# MtMake
MultiThreaded Make wrapper. The idea is to build a dependency graph and
compile the nodes on different threads.

# Requirements
 - Python 3.4 - 3.5
 - [pip](https://pypi.python.org/pypi/pip)
 - [virtualenv](https://pypi.python.org/pypi/virtualenv)
 - [argument](https://pypi.python.org/pypi/argument)
 - [nose](https://pypi.python.org/pypi/nose)

# Setting up the development environment

 - ```$ virtualenv -p /usr/bin/python3.4 venv```
 - ```$ source venv/bin/activate```
 - ```$ pip3 install -r requirements.txt```
 - Do development!
 - ```$ deactivate```

# License
mtmake is licensed under the MIT license, see the [LICENSE](LICENSE) file for
details.
