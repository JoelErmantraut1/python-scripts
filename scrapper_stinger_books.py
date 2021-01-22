#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Author: Joel Ermantraut
Last Modification: 22/01/2020
Python Version: 3.9.1
Last Working Test: 22/01/2020

This scripts gets each link in a document, and goes to it to
download its content. This was designed for a specific file
format, and a specific web page, so it will be useful only
"""

import os
import PyPDF2
import requests
from bs4 import BeautifulSoup

def mostrar_links(page_number):
    pdf_file = open('file.pdf', 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)

    page = read_pdf.getPage(page_number)
    page_content = page.extractText().split('\n')

    links = {}

    for line_index in range(0, len(page_content)):
        # Next line after number is title
        line = page_content[line_index]
        try:
            if (int(line) < 500):
                title = page_content[line_index + 1]
        except ValueError:
            if 'http' in line:
                links[title] = line

    for link in links.keys():
        print(link + '\t:\t' + links[link])

def get_links(page_number):
    pdf_file = open('file.pdf', 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)

    page = read_pdf.getPage(page_number)
    page_content = page.extractText().split('\n')

    links = {}

    for line_index in range(0, len(page_content)):
        line = page_content[line_index]
        try:
            if (int(line) < 500):
                title = page_content[line_index + 1]
        except ValueError:
            if 'http' in line:
                links[title] = line

    return links

def download(links):
    for link in links.keys():
        print(link)
        page = requests.get(links[link])

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(class_='c-button c-button--blue c-button\
                __icon-right test-download-book-options test-bookpdf-link')
        if results == None:
            results = soup.find(class_='c-button c-button--blue c-button__icon-right test-bookpdf-link')

        try:
            pdf_link = results.get('href')
            pdf_file = requests.get('https://link.springer.com/' + pdf_link)
            open('pdfs/{0}.pdf'.format(link), 'wb').write(pdf_file.content)
        except:
            print("ERROR:\t" + link)

def main():
    for i in range(4, 21):
        print("Page Number:  ", i)
        links = get_links(i)
        download(links)

main()
