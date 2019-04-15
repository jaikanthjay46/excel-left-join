# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import os

import xlrd
from django import forms
from django.core.files.storage import FileSystemStorage
from django.http import (HttpResponse, HttpResponseRedirect,
                         StreamingHttpResponse)
from django.shortcuts import render
from setuptools.command.upload import upload

from .models import Price, Product


def index(request):
    return render(request, 'index.html')

def csv_from_excel():

	wb = xlrd.open_workbook('tmp.xlsx')
	sh = wb.sheet_by_index(0)
	your_csv_file = open('tmp.csv', 'w+')
	wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
	for rownum in range(1,sh.nrows):
		wr.writerow(sh.row_values(rownum))

	your_csv_file.close()

BATCH_SIZE = 20
def handle_uploaded_file(f):
	try:
		os.remove("tmp.csv")
		os.remove("tmp.xlsx")
	except:
		pass
	
	with open('tmp.'+f.name.split('.')[-1]  , 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	
	if(f.name.split('.')[-1] == 'xlsx'):
		csv_from_excel()
	
	with open('tmp.csv','r') as csvfile:
		fin = csv.reader(csvfile, delimiter=",")
		for row in fin:
			if(len(row) > 0):
				obj = Product(sku=row[0],asin=row[1],quantity=float(row[2]),price= float(row[3]))
				obj.save()

def handle_uploaded_file2(f):
	try:
		os.remove("tmp.csv")
		os.remove("tmp.xlsx")
	except:
		pass
	
	with open('tmp.'+f.name.split('.')[-1]  , 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	
	if(f.name.split('.')[-1] == 'xlsx'):
		csv_from_excel()
	
	with open('tmp.csv','r') as csvfile:
		fin = csv.reader(csvfile, delimiter=",")
		for row in fin:
			if(len(row) > 0):
				obj = Price(product_id=row[0],quantity=float(row[1]),price= float(row[2]))
				obj.save()	
		


def upload(request):
	if request.method == 'POST' and request.FILES['file']:
		myfile = request.FILES['file']
		handle_uploaded_file(myfile)
	return HttpResponse('success')

def upload2(request):
	if request.method == 'POST' and request.FILES['file']:
		myfile = request.FILES['file']
		handle_uploaded_file2(myfile)
	return HttpResponseRedirect('/view')

def read(request):
	p = Product.objects.raw(""" SELECT b.product_id,a.sku,a.asin,b.price,b.quantity FROM 'elj_app_product' as a,'elj_app_price' as b where a.sku LIKE (b.product_id || '%') ORDER BY b.product_id """)
	pseudo_buffer = Echo()
	writer = csv.writer(pseudo_buffer)
	response = StreamingHttpResponse((writer.writerow([r.product_id,r.sku,r.asin,r.price,r.quantity]) for r in p),content_type="text/csv")
	response['Content-Disposition'] = 'attachment; filename="result.csv"'
	return response

class Echo:

	def write(self, value):
		return value
