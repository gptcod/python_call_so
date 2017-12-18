#!/usr/bin/python
# -*- coding: utf-8 -*-

from ctypes import *
import ctypes
from subprocess import *
import subprocess
import re

def mkdir_officex():
	args = "ls /home/venus/apt/cloud/officextemp/"
	return_object = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
	error_log = return_object.stderr.read()

	if error_log != None:
		#print 123
		args = "mkdir -v -p /home/venus/apt/cloud/officextemp/"
		command_object = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
		output_log = command_object.stdout.read()
		#print output_log

def get_file_type(so_file_path, check_file_path):
	
	#methods = subprocess.check_output(['nm', '-D', 'libfiltertype.so'])     
	#args =['nm','-D', 'libfiltertype.so']                                   
	args="nm -D libfiltertype.so"                                            
	methods = Popen(args,stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)
      
	pattern = re.compile(r'(_.*checktype[A-Z].*)')          
	temp = methods.stdout.read()                          
	checktype_method = pattern.findall(temp)[0]
	#print 123, checktype_method
          
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
	#print filetype
	return filetype

print get_file_type("./libfiltertype.so","/home/wt/libfiltertype.so")
mkdir_officex()
