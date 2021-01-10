# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""

Este algoritmo se ejecuta en segundo plano y realiza una limpieza
periodica del escritorio, copiando los archivos de este a un 
directorio auxiliar

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