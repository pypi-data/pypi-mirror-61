MusicRaft
=========

'MusicRaft' is an GUI for the ABC(plus) music notation, built around python and the Qt GUI toolkit. It is in fact a very lightweight (and very limited!) IDE
 implemented as 'the raft' on top of which the plugin 'abcraft' is created. (Actually,
 the architechtural split isn't quite so clean; the raft contains quite some ABC-specific code!)

![Alt text](https://gitlab.com/papahippo/MusicRaft/raw/master/screenshots/Musicraft_017.png?raw=true "Editing ABCplus music source while viewing graphical ouput")

A separate plugin `pyraft` supports editing of python3 source files. When a python script writes output with an HTML header,
pyraft dsiplays the HTML in a special 'Html' tab within  the display notebook. This is present in the
'git' project but absent in the python package, in order to keep the number of dependencies
on other packages to a minimum.

##Installation

The 'official' way to install is musicraft is to use the python package repository.
The exact syntax will vary across platforms but will be something like...

`python3 -m pip install musicraft`

after which starting musicraft is a simple matter of ...

`python3 -m musicraft [abc source file name ...]` 
 
 .. or something very similar. 

It is possible to associate this action with all `.abc` files so that a 
double-click on such a file in the file manager is sufficient to start
musicraft. How to do this depends on the operating systemcontext; perhaps
this will be (semi)- automated in later releases of the musicraft
package.

A few start-up scripts are also included. These are really a left-over from
the time before I got the '-m' approach working but are left in as potentially
useful. Where exactly these get installed - and whether that location
is conveniently within the execution path - depends on your OS and system set-up.  
###Environment

More 'on the go' debug information can be obtained by setting...
* `MUSICRAFT_DBG = 1`

... before starting musicraft. Inevitably, perhaps, the choice of what
debug info to output is governed by my issues encountered recently not by
your issues encountered today, so this is not guaranteed to be helpful!  

Musicraft was originally designed to work with `Qt4` via either `PyQt4` or
`PySide`. This software is however becoming more and more deprecated in
favour of `Qt5` via either `PySide2` or `PyQt5`. Accordingly, Musicraft has
been reworked to support these; indeed, musicraft `PySide2` is now used
by default. This behaviour can however be overruled by settinging an
environment variabe:

* `MUSICRAFT_QT = PyQt4`
* `MUSICRAFT_QT = PySide`
* `MUSICRAFT_QT = PyQt5`

Not overruling this setting is treated as equivalent to...

* `MUSICRAFT_QT = PySide2`

__Important note regarding 'Qt' dependencies:__

The musicraft package specifies `PySide2` as a dependency, so it gets installed
whether you like it or not. This is only likely to be  problem if you're
running on a very old OS version that doesn't support `PySide2`, `Qt5` etc.
In this case, you may wish to pu t your own package together, baed on
the code in this repository.  

Recent OS versions (e.g. Ubuntu Linux 18.04, Windows 10) may only
suport 'Qt5', not the older, deprecacted 'PyQt4'. In some cases, there is
a workaround for this. For example, on Ubuntu 18.04 one can install
PySide by:

`sudo apt-get install python3-pyside`

####Standalone binaries

I have created (using PyInstaller) standalone executables of Musicraft for 64-bit systems under
[Windows](https://gitlab.com/papahippo/MusicRaft/blob/master/dist/win_musicraft.exe) (tested on Windows 10) 
and under [Linux](https://gitlab.com/papahippo/MusicRaft/blob/master/dist/lin_musicraft) (tested under Ububtu 18.04). 
 