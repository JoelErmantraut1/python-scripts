#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""

A este algoritmo se le asignan dos carpetas, una que es la que se debe copiar
y la otra sobre la cual se debe copiar. La idea es que la primer carpeta
quede exactamente igual a la segunda, pero realizando la menor cantidad de
modificaciones posibles y a la maxima velocidad. Para esto, debe analizar 
al nivel de carpeta e ir adentrandose recursivamente.

"""
import shutil
import glob
import os
from tkinter import *
from tkinter import filedialog

base_url = None
destino_url = None

def verificar_archivos(base, destino):
	archivos_destino = glob.glob(destino + '\\*.*')
	archivos_base = glob.glob(base + '\\*.*')

	for i in archivos_destino:
		if not i.split('\\')[-1] in [i2.split('\\')[-1] for i2 in archivos_base]:
			# Borrar archivos sobrantes
			os.remove(i) # Borra el archivo de la carpeta destino
			archivos_destino = glob.glob(destino + '\\*.*')

	if len(archivos_destino) == len(archivos_base):
		return
		# Si borramos los archivos sobrantes y tienen la misma cantidad deben de ser los mismos archivos
		# Terminamos con esta carpeta y nos vamos

	# Si no lo que puede pasar es que haya menos archivos
	# Pasamos entonces a buscar cuales son los archivos que estan en la carpeta
	# de "Base" pero no de "Destino"

	for i in archivos_base:
		if not i.split('\\')[-1] in [i2.split('\\')[-1] for i2 in archivos_destino]:
			with open(i, 'rb') as base_file:
				with open(destino + '\\' + i.split('\\')[-1], 'wb') as destino_file:
					shutil.copyfileobj(base_file, destino_file)

			archivos_destino = glob.glob(destino + '\\*.*')
			# Copio el archivo en la carpeta destino

			if len(archivos_destino) == len(archivos_base):
				return
			# Vuelvo a verificar para ahorrar tiempo

def recorrer(base, destino):
	archivos_destino = glob.glob(destino + '\\*')
	archivos_base = glob.glob(base + '\\*')

	for i in archivos_base:
		if os.path.isdir(i):
			if i.split('\\')[-1] in [i2.split('\\')[-1] for i2 in archivos_destino]:
				# Si el directorio esta, los paso ambos
				# a la funcion para que la trabaje
				recorrer(i, destino + '\\' + i.split('\\')[-1])
			else:
				# Copia el directorio completo tal cual esta en "Base"
				shutil.copytree(i, destino + '\\' + i.split('\\')[-1])
	for i in archivos_destino:
		if os.path.isdir(i):
			if not i.split('\\')[-1] in [i2.split('\\')[-1] for i2 in archivos_base]:
				shutil.rmtree(os.path.abspath(i)) # Borra el directorio completo

	verificar_archivos(base, destino)

def file_dialog_base():
	global base_url

	base_url = filedialog.askdirectory()

def file_dialog_destino():
	global destino_url

	destino_url = filedialog.askdirectory()

def interface():
	root = Tk()
	root.title("Actualizador")
	root.geometry("300x100")

	Button(root, text="Carpeta base", command=file_dialog_base).pack(fill=BOTH, expand=YES)
	Button(root, text="Carpeta destino", command=file_dialog_destino).pack(fill=BOTH, expand=YES)
	Button(root, text="Actualizar", command=lambda: recorrer(base_url, destino_url)).pack(fill=BOTH, expand=YES)

	root.mainloop()

def main():
	interface()

main()