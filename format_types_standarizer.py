#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Author: Joel Ermantraut
Last Modification: 22/01/2020
Python Version: 3.9.1
Last Working Test: 10/02/2019

This programs was made to standardize the content of a heavy folder
with lot of files of different extension. Some of the file extension
included in that folder were:

    - zip, rar
    - doc, docx, ppt, pptx
    - txt, epub

This file convert file to PDF, if there are installed programs
of Microsoft Office. Also, extract compressed files.
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
    doc.SaveAs(name, FileFormat = 17) # 17, selects format
    doc.Close()

def listar_directorios(path):
    dirs = glob.glob(path + "**/*")
    for i in dirs:
        if os.path.isdir(os.path.abspath(i)):
            listar_directorios(os.path.abspath(i))
        else:
            ext = i.split('.')[-1]
            ext = ext.lower() # Simplifies comparation
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
                        pass # This happens when files are read-only
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
    init_URL = os.getcwd()
    list_directories(URL_inicial)
    word.Quit()
    powerpoint.Quit()

main()
