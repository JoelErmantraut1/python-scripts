# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Author: Joel Ermantraut
Last Modification: 22/01/2020
Python Version: 3.9.1
Last Working Test: 22/01/2020

This programs execute himself in background and cleans the desktop
each time a file appear (to keep it empty) and sends it to a folder.
"""

from glob import glob
from shutil import copytree, copy, rmtree
from os import path, remove
from threading import Timer

dest = "C:\\Users\\joele\\OneDrive\\Documentos\\Centro"

def mover():
    directorio = glob("C:\\Users\\joele\\Desktop\\*")

    for i in directorio:
        try:
            if path.isdir(i):
                copytree(i, dest + "\\" + path.basename(i))
                rmtree(i)
            else:
                copy(i, dest + "\\" + path.basename(i))
                remove(i)
            print("Movido: {0}.".format(i))
        except FileExistsError as e:
            print("Ya existente: {0}.".format(i))

    print("Escritorio limpio")

    Timer(10.0, mover).start()

def portal():
	mover()

portal()
