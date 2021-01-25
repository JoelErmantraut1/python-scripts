# -*- coding: utf-8 -*-

"""
Author: Joel Ermantraut
Last Modification: 23/01/2020
Python Version: 3.9.1
Last Working Test: 23/01/2020

This program calculates the sum of a list of tickets, in PDF.
It was writted in Spanish because the customer wanted it.
"""
import os
import re
import json
import time
import glob
import PyPDF2
import subprocess
import os.path

folder_dir = os.path.expanduser('~')
faltantes = [
    [], [], [], [], [], [], [], [], [], [], [], [] # 1 each month
] # Missing tickets list
last_number = 0
cache_filename = "files_cache.json"

def get_pdf_number(url):
    name = url.split('\\')[-1].split('.')[-2]
    return int(name.split("_")[-1])

def get_num(url):
    global faltantes, last_number

    suma_dia = 0
    pdf_file = open(url, 'rb')
    try:
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
    except Exception as e:
        print("EL PDF{0} ESTA DAÑADO.\n".format(url))
        return 0,0,0

    if read_pdf.isEncrypted:
        read_pdf.decrypt('')

    page = read_pdf.getPage(0)
    page_content = page.extractText()

    fecha = page_content.split("Domicilio:")[1]
    fecha = fecha.split("20177125858")[0]
    fecha = fecha.split('/')
    dia = int(fecha[0])
    mes = int(fecha[1])
    anio = int(fecha[2]) - 2000

    for i in ['unidades', '1000 kWh', 'pares', 'litros']:
        # This is a kind of hack, because this are common
        # values that it takes when the user makes a mistake.
        try:
            page_content = page_content.split(i)[1].split('Subtotal')[0]
        except IndexError:
            continue

    num = page_content.split(',')[0]
    decimal = page_content.split(',')[1][0:2]
    num = float(num + '.' + decimal)

    boleta_num = get_pdf_number(url)
    if last_number == 0:
        last_number = boleta_num
    else:
        last_number += 1
        if last_number != boleta_num:
            faltantes[mes - 1].append(last_number)
            last_number = boleta_num

    return dia, mes, num

def file_in_cache(url):
    global cache_filename

    if not os.path.exists(cache_filename):
        with open(cache_filename, 'w') as file:
            json.dump(dict(), file)

    else:
        with open(cache_filename, 'r') as file:
            cache_dict = json.load(file)

            for key in cache_dict.keys():
                if key == str(get_pdf_number(url)):
                    return cache_dict[key]

    return None

def add_cache_files(url, value):
    global cache_filename

    cache_dict = None

    with open(cache_filename, 'r') as file:
        cache_dict = json.load(file)

    cache_dict[str(get_pdf_number(url))] = value

    with open(cache_filename, 'w') as file:
        json.dump(cache_dict, file, indent = 4)

def main():
    global last_number, faltantes

    archivos = glob.glob(folder_dir + '*')
    # Firstly, deletes duplicated files
    print("Limpiando duplicados...")
    for i in range(len(archivos)):
        x = re.search(r"\(\d+\)", archivos[i])
        # Watches one by one for number at the end of the name (1), (2), etc.
        if x != None:
                os.remove(archivos[i])

    print("Calculando...")
    archivos = subprocess.Popen(
            ["ls", "-p", folder_dir],
            stdout=subprocess.PIPE,
    ).stdout
    # This was needed because Python didn't list all files
    suma_dia = 0
    suma = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cantidad = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in archivos:
        i = folder_dir + i[:-1].decode()

        if i.split(".")[-1].lower() != 'pdf':
            continue

        cache = file_in_cache(i)
        if cache != None:
            dia, mes, num = cache
        else:
            dia, mes, num = get_num(i)
            add_cache_files(i, [dia, mes, num])

        if dia == 0 and mes == 0 and num == 0:
            # File wasn't PDF or was corrupted	
            continue

        suma[mes - 1] += num
        cantidad[mes - 1] += 1

        if dia == int(time.strftime("%d")) and mes == int(time.strftime("%m")):
            suma_dia += num

    meses = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre"
    ]
    print("\nTotales:\n")
    for mes in range(len(meses)):
        print("Total para el mes de {0}:{2} {1}".format(meses[mes], round(suma[mes], 2), " " * (25 - len(meses[mes]))))

    print("\nTotal del día ({0}/{1}/{2}): {3}".format(
        time.strftime("%d"),
        time.strftime("%m"),
        time.strftime("%y"),
        suma_dia
    ))

    print("\nBoletas Faltantes:\n")
    for mes in range(len(meses)):
        print("Faltantes para el mes de {0}:{2}  {1}".format(meses[mes], faltantes[mes], " " * (20 - len(meses[mes]))))

    print("\nTotal Estimado Tomando Boletas Faltantes:\n")
    for mes in range(len(meses)):
        estimado = 0
        if cantidad[mes] > 0:
                estimado = len(faltantes[mes]) * (suma[mes] / cantidad[mes])
        print("Totales para el mes de {0}:{2} {1}".format(meses[mes], round(suma[mes] + estimado, 2), " " * (24 - len(meses[mes]))))

    input("Presionar ENTER para cerrar")

main()
