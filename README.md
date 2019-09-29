# FIDI
 Program for static analysis for shields and plates using  finite-difference methods (FDM)

## Folders structure

* docs - folder for documentation
* sandbox - folder for playing with source
* src  - main source folder

Python packages
-------------------------

FIDI is written in Python 3, that is necessary in order to run the program,
in addition some parts of source may need additional modules.

List of necessary python packages in order to run FIDI :
* NumPy
* PySide2
* Matplotlib

Installation
------------

At this moment program is made from 2 separate parts - GUI and file gathering and
saving data from user.

There is no ready to use setup file for GUI yet, however you may run it directly
by execution source code.
To run GUI download fidi_gui.py and Ui folder from gui_core.py located in FIDI/src/fidi_gui
then save them in the same location. Now you are able to launch the program by compiling 
fidi.gui.py in Python 3. 

To run part of program responsible for gathering and saving data from user, you have to 
download and save in the same location content of fidi_attributes folder located in FIDI/src,
then you may run saving_attributes.py or loading_attributes, for more information check guide
in FIDI/docs.

Contribute
----------

- Issue Tracker: github.com/mateuszac/FIDI/issues
- Source Code: github.com/mateuszac/FIDI

License
-------

The project is licensed under the GNU General Public License v3.0.