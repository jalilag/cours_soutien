from cx_Freeze import setup,Executable
import os,sys

os.environ['TCL_LIBRARY'] = r'C:/Users/agoum/AppData/Local/Programs/Python/Python37/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = r'C:/Users/agoum/AppData/Local/Programs/Python/Python37/tcl/tk8.6'

excludes = ['Tkinter']
includes = ["sys","functools","time","os","PyQt5","sys","math","pynput","pandas","numpy"]  # nommer les modules utilises
packages = ["py_lib","public","numpy"]  # nommer les packages utilises

includefiles = ["css","tcl86t.dll","remote.ico","tk86t.dll","start.bat"]


# niveau d'optimisation pour la compilation en bytecodes
optimize = 0

# si True, n'affiche que les warning et les erreurs pendant le traitement cx_freeze
silent = True

path = sys.path
path.append('C:/Users/agoum/Documents/Programmation/python/remote_msgs')

# construction du dictionnaire des options
options = {"path": path,
          "packages": packages,
          "excludes":excludes,
          "includes":includes,
          "include_files": includefiles,
          "optimize": optimize,
          "silent": silent,
          # "namespace_packages":['zope'],
          }

target = Executable(
    script="remote_msgs.py",
    base="Win32GUI",
    icon = "remote.ico",
    )

setup(
	name = "Remote msgs",
	version = "3.0",
	description = "Envoi automatique de message sur whatsapp",
	author="Jalil AGOUMI",
  author_email="agoumi.jalil@gmail.com",
	options={"build_exe": options},
	executables = [target],
	)