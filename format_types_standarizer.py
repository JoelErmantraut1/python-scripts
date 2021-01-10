#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""

Este algoritmo se diseño con la finalidad de estandarizar el contenido
de una carpeta muy pesada que contenia archivos en multiples formatos,
tales como comprimidos (zip, rar), documentos(doc, docx, ppt, etc), 
texto (txt), y algunos otro formatos menos comunes.

Los formatos que menos frecuentes podian ser convertidos manualmente,
pero los demas, debido a la abundancia y complejidad requirieron
automatizacion. En conclusion, este algoritmo analiza los formatos
de una carpeta elegida y las contenidas en esta, y transforma los
formatos mas comunes a PDF, si en el equipo en el que se ejecutan
se encuentran instaladas algunas herramientas populares como
Microsoft Word, Microsoft PowerPoint, entre otras.

"""

import os
import sys
import glob
import zipfile
import os.path
import win32com.client
import pywintypes
import codecs

word = win32com.client.gencache.EnsureDispatch("Word.Application")
word.Visible = 0
powerpoint = win32com.client.Dispatch("Powerpoint.Application")
powerpoint.Visible = 1

def powerpointToPDF(path, name):
	deck = powerpoint.Presentations.Open(os.path.abspath(path))
	deck.SaveAs(name, FileFormat = 32)
	deck.Close()

def textToPDF(name, text):
	doc = word.Documents.Add() # Create new Document Object
	doc.PageSetup.Orientation = 1 # Make some Setup to the Document:
	doc.PageSetup.LeftMargin = 20
	doc.PageSetup.TopMargin = 20
	doc.PageSetup.BottomMargin = 20
	doc.PageSetup.RightMargin = 20
	doc.Content.Font.Size = 14
	doc.Content.Paragraphs.TabStops.Add(100)
	doc.Content.Text = text
	doc.Content.MoveEnd()
	doc.SaveAs(name, FileFormat = 17)
	doc.Close(SaveChanges = 0) # Close the Word Document (a save-Dialog pops up)

def wordToPDF(path, name):
	doc = word.Documents.Open(os.path.abspath(path))
	doc.SaveAs(name, FileFormat = 17) # 17 es el formato que funciona
	doc.Close()

def listar_directorios(path):
	dirs = glob.glob(path + "**/*")
	for i in dirs:
		if os.path.isdir(os.path.abspath(i)):
			listar_directorios(os.path.abspath(i))
		else:
			ext = i.split('.')[-1]
			ext = ext.lower() # La ponemos en minusculas para simplificar la comparacion
			if (ext == "zip"):
				print(i)
				archivo_zip = zipfile.ZipFile(i)
				archivo_zip.extractall(path)
				archivo_zip.close()
				os.remove(i)
			elif (ext == "doc" or ext == "docx"):
				if (i[0:2] == '~$'):
					continue
				print(i)
				name = os.path.abspath(i).split('.')
				name.pop()
				name = ' '.join(name)
				name = name + '.pdf'
				try:
					wordToPDF(i, name)
					os.remove(i)
				except pywintypes.com_error:
					pass # Este error se produce cuando esta configurado para solo lectura
			# Los que no lo estan, es porque estan protegidos
			elif (ext == 'ppt' or ext == 'pptx'):
				print(i)
				name = os.path.abspath(i).split('.')
				name.pop()
				name = ' '.join(name)
				name = name + '.pdf'

				powerpointToPDF(i, name)

				os.remove(i)
			elif (ext == 'txt'):
				print(i)

				with codecs.open(i, 'r', 'latin-1' ) as file:
					text = file.read()

				name = os.path.abspath(i).split('.')
				name.pop()
				name = ' '.join(name)
				name = name + '.pdf'

				textToPDF(name, text)

				os.remove(i)

def main():
	URL_inicial = os.getcwd()
	listar_directorios(URL_inicial)
	word.Quit()
	powerpoint.Quit()

main()