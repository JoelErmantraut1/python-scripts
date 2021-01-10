#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Este algoritmo genera una biblia en formato "xmm", que es un estandar
de biblias open source.

IMPORTANTE: Tomar en cuenta que se utiliza una pagina WEB, la cual se
parsea para obtener la informacion necesaria y se guarda en el archivo.
Si esta pagina modifico su estructura, habria que modificar el algoritmo. 
"""

import requests
from bs4 import BeautifulSoup

libros_list = [
	"Génesis",
	"Éxodo",
	"Levítico",
	"Números",
	"Deuteronomio",
	"Josué",
	"Jueces",
	"Rut",
	"1 Samuel",
	"2 Samuel",
	"1 Reyes",
	"2 Reyes",
	"1 Crónicas",
	"2 Crónicas",
	"Esdras",
	"Nehemías",
	"Ester",
	"Job",
	"Salmos",
	"Proverbios",
	"Eclesiastés",
	"Cantares",
	"Isaías",
	"Jeremías",
	"Lamentaciones",
	"Ezequiel",
	"Daniel",
	"Oseas",
	"Joel",
	"Amós",
	"Abdías",
	"Jonás",
	"Miqueas",
	"Nahúm",
	"Habacuc",
	"Sofonías",
	"Hageo",
	"Zacarías",
	"Malaquías",
	"Mateo",
	"Marcos",
	"Lucas",
	"Juan",
	"Hechos",
	"Romanos",
	"1 Corintios",
	"2 Corintios",
	"Gálatas",
	"Efesios",
	"Filipenses",
	"Colosenses",
	"1 Tesalonicenses",
	"2 Tesalonicenses",
	"1 Timoteo",
	"2 Timoteo",
	"Tito",
	"Filemón",
	"Hebreos",
	"Santiago",
	"1 Pedro",
	"2 Pedro",
	"1 Juan",
	"2 Juan",
	"3 Juan",
	"Judas",
	"Apocalipsis"
]

cap_list = [
	50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4, 28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22
]

def get_verses(file, book, cap):
	verses = []

	URL = 'https://www.biblegateway.com/passage/?search={0}+{1}%3A1&version=RVA-2015'.format(libros_list[book], cap)

	page = requests.get(URL)

	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find(class_='version-RVA-2015 result-text-style-normal text-html')

	p_elems = results.find_all('p')
	for p in p_elems:
		span_elems = p.find_all('span')
		for span in span_elems:
			try:
				texto = span.text.split('\xa0')[1]
			except IndexError:
				texto = span.text
			verses.append(texto)

	try:
		verses.pop(1) # El segundo item solo es el numero de capitulo
	except IndexError:
		pass
	for i in range(len(verses)):
		file.write('      <v n="{0}">\n'.format(i + 1))
		file.write(verses[i])
		file.write(' </v>\n')

def main():
	file = open('Reina-Valera Actualizada.xmm', 'w')

	file.write('<?xml version="1.0"?>\n')
	file.write('<bible>\n')

	for book in range(len(libros_list)):

		file.write('  <b n="{0}">\n'.format(libros_list[book]))

		capitulos = range(1, cap_list[book] + 1)
		for cap in capitulos:
			print("{0}: {1}".format(libros_list[book], cap))
			file.write('    <c n="{0}">\n'.format(cap))
			get_verses(file, book, cap)
			file.write('    </c>\n')

		file.write('  </b>\n')

	file.write('</bible>\n')

	file.close()

main()