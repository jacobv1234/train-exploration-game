from os import system
# this file runs the nuitka command so it's not forgotten
system('python -m nuitka --standalone --windows-icon-from-ico=icon.ico --onefile --output-filename="Untitled Train Game.exe" --enable-plugin=tk-inter main.py')