# pip install request BeautifulSoup4 pdfplumber pandas pypdf2 fpdf2 pypdf2
import requests
import urllib.request
from bs4 import BeautifulSoup

from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader

import re
import sys
import pdfplumber
import pandas as pd
import time

# DOWNLOAD FILE
domain = 'https://www.pref.okinawa.lg.jp'
url = domain + '/site/hoken/chiikihoken/kekkaku/press/20200214_covid19_pr1.html'
response = requests.get(url)

def remove_invisible_chars(chars):
    for char in chars:
        if char['non_stroking_color'] == (1,1,1):
            print(char)

## Get file link and change file name
soup = BeautifulSoup(response.text, "html.parser")
link = soup.find(id="tmp_contents").find_all('a')[0]['href']

# find_pattern = r"\/documents\/(?P<report>\d*)\D*(?P<cases>\d*)\D*.pdf"
# replace_pattern = lambda number: number.group('report') + '_' + number.group('cases') + '.pdf'

filename = link[link.find('documents/')+10:].replace('hou', '_').replace('rei', '').replace('me', '')

## Download the file
download_url = domain + link
urllib.request.urlretrieve(download_url, './pdf/' + filename)
print("PDF downloaded at: pdf/" + filename)

# Preprocess PDF

## Create lines
linePDF = FPDF()
linePDF.add_page(orientation='P', format='A4')
linePDF.set_fill_color(0,0,0)
linePDF.rect(34,275,156,0.5,'F')
linePDF.add_page()
linePDF.set_fill_color(0,0,0)
linePDF.rect(34,281.5,156,0.5,'F')
linePDF.output('component/line.pdf', 'F')

## Add lines to every page
outputPDF = PdfFileWriter()
sourcePDF = PdfFileReader(open('./pdf/' + filename, "rb"))

# print how many pages sourcePDF has:
# print (sourcePDF.numPages)
linePDF = PdfFileReader(open("component/line.pdf", "rb"))

for pageNum in range(sourcePDF.numPages):
    if pageNum == 2:
        linePlace = linePDF.getPage(0)
    else :
        linePlace = linePDF.getPage(1)

    if pageNum >= 2:
        currentPage = sourcePDF.getPage(pageNum)
        currentPage.mergePage(linePlace)
        outputPDF.addPage(currentPage)
## finally, write "outputPDF" to document-outputPDF.pdf
outputPDFStream = open('./pdf/processed_latest.pdf', "wb")
outputPDF.write(outputPDFStream)

print ('PDF preprocess finished')