from os import system
# this file runs the pyinstaller command so it's not forgotten
system('pyinstaller -n "Untitled Train Game" --onefile --windowed -i "icon.ico" main.py')