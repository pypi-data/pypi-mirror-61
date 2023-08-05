MusicRaft
=========

'MusicRaft' is an GUI for the ABC(plus) music notation. Its implementation went through a few incarnations:

 Musicraft is built around PySide. It is in fact a very lightweight (and very limited!) IDE
 implemented as 'the raft' on top of which the plugin 'abcraft' is created. (Actually,
 the arcitechtural split isn't quite so clean; teh raft contains quite some ABC-specific code!)

![Alt text](https://gitlab.com/papahippo/MusicRaft/raw/master/screenshots/Musicraft_017.png?raw=true "Editing ABCplus music source while viewing graphical ouput")

A separate plugin 'pyraft' supports editing of python3 source files. When a python script writes output with an HTML header,
pyraft dsiplays the HTML in a special 'Html' tab within  the display notebook. This is present in the
'git' project but absent in the python package, in order to keep the number of dependencies
on other packages to a minimum.

##Installation

The 'official' way to install is musicraft is to use the python package repository.
The exact syntax will vary across platforms but will be something like...

_python3 -m pip install musicraft_

after which starting musicraft is a simple matter of (on Windows)...

_win_musicraft.py_   or perhaps e.g. _C:\path\to\python\dir\python.exe_ _win_musicraft.py_

... or (on Linux) ...
 
 _lin_musicraft.py_
 
 .. or something very similar. 

recent Linux versions (e.g. Ubuntu 18.04) may give an error when tring to satisfy the dependency
on Pyside, which is, strictly speaking, not supported on python3.5 or later.
The workaround for this is to install PySide first, using the apppropriate Linux pakcage manager,
e.g. (on Ubuntu):

sudo apt-get install python3-pyside

Installation on Windows 10 can also be problematical because of an incompatibility in MSVC run-time library versions.
I don't have a quick and easy workaround for this except .... (see below!)

####Standalone binaries

I have created (using PyInstaller) standalone executables of Musicraft for 64-bit systems under
[Windows](https://gitlab.com/papahippo/MusicRaft/blob/master/dist/win_musicraft.exe) (tested on Windows 10) 
and under [Linux](https://gitlab.com/papahippo/MusicRaft/blob/master/dist/lin_musicraft) (tested under Ububtu 18.04). 
 