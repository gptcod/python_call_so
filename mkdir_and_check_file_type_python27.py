#!/usr/bin/python
# -*- coding: utf-8 -*-

from ctypes import *
import ctypes
import subprocess
import re

def mkdir_officex():
	ls_log = subprocess.check_output(['ls', '-l', '/home/venus/apt/cloud/officextemp/'])
	if ls_log.find("cannot access") != -1:
		result = subprocess.check_output(['mkdir', '-p', '/home/venus/apt/cloud/officextemp/'])
		print result

def get_file_type(so_file_path, check_file_path):

	methods = subprocess.check_output(['nm', '-D', 'libfiltertype.so'])
	pattern = re.compile(r'(_.*checktype[A-Z].*)')
	checktype_method = pattern.findall(methods)[0]

	so_file = cdll.LoadLibrary(so_file_path)

	with open(check_file_path) as file:
		data = file.read()

	data_list = list(data)
	data_array = (ctypes.c_char * len(data_list))(*data_list)

	p = create_string_buffer(10)

	check_file_name = check_file_path.split("/")[-1]

	so_file[checktype_method](byref(data_array), len(data_list), p, check_file_name)

	filetype = ""

	for i in p.raw:
		if (ord)(i) != 0:
			filetype += i

	return filetype

#print get_file_type("./libfiltertype.so", "./new.txt")
print mkdir_officex()
