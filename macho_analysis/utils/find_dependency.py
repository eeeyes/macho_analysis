# -*- coding: utf-8 -*-

import subprocess;

import re;

import os;

import sys;

class MachoProduct:

	def __init__(self,lib_path):
	
		self.lib_path = lib_path;
		
	def allUndefinedSymbols(self):
	
		nm_cmd = ['nm','-arch','armv7','-u',self.lib_path];

		nm_cmd_output = subprocess.Popen(nm_cmd,stdout=subprocess.PIPE).communicate();

		undefined_symbols = nm_cmd_output[0].split('\n');

		symbols = set();

		for undefined_symbol in undefined_symbols:

			undefined_symbol = undefined_symbol.strip();
	
			empty_line_pattern = re.compile(r'^\s+$');
	
			path_pattern = re.compile(r':$');
	
			#ignore empty line
	
			if not len(undefined_symbol):
	
				continue;
	
			#ignore empty line
		
			if empty_line_pattern.search(undefined_symbol):
	
				continue;
	
			#ignore file path 
	
			if path_pattern.search(undefined_symbol):
	
				continue;
		
			symbols.add(undefined_symbol);
					
		return symbols;
		
	def allDefinedSymbols(self):	
			
		nm_cmd = ['nm','-arch','armv7','-U',self.lib_path];

		nm_cmd_output = subprocess.Popen(nm_cmd,stdout=subprocess.PIPE).communicate();

		defined_symbols = nm_cmd_output[0].split('\n');

		symbols = set();
		
		for defined_symbol in defined_symbols:

			defined_symbol = defined_symbol.strip();
	
			empty_line_pattern = re.compile(r'^\s+$');
	
			path_pattern = re.compile(r':$');
	
			symbol_pattern = re.compile(r'\S+\s+\S+\s+(.+)$');
			
			#ignore empty line
	
			if not len(defined_symbol):
	
				continue;
	
			#ignore empty line
		
			if empty_line_pattern.search(defined_symbol):
	
				continue;
	
			#ignore file path
	
			if path_pattern.search(defined_symbol):
	
				continue;
		
			symbol_match = symbol_pattern.search(defined_symbol);
			
			defined_symbol = symbol_match.groups()[0];
			
			symbols.add(defined_symbol);
			
		return symbols;

def findDependency(lib_path_array):

	lib_symbol_array = [];
	
	#get symbols from libs
	
	for lib_path in lib_path_array:
	
		lib_name = os.path.basename(lib_path);
		
		macho_product = MachoProduct(lib_path);
		
		defined_symbols = macho_product.allDefinedSymbols();
	
		un_defined_symbols = macho_product.allUndefinedSymbols();
	
		lib_symbol_array.append((lib_name,defined_symbols,un_defined_symbols));
		
	
	#遍历所有库的未定义符号
			
	for (lib_name,defined_symbols,undefined_symbols) in lib_symbol_array:

		depend_lib_set = set();
	
		depend_lib_symbol_hash = dict();
	
		print '======================='
	
		print lib_name;
	
		print '-----------------------'
	
		for undefined_symbol in undefined_symbols:
	
			for (a_lib_name,a_defined_symbols,_) in lib_symbol_array:
		
				if lib_name == a_lib_name:
			
					continue;
				
				if undefined_symbol in a_defined_symbols:
			
					depend_lib_set.add(a_lib_name);
				
					depend_lib_symbol_hash[a_lib_name] = undefined_symbol;
				
					break;			
	
		for depend_lib in depend_lib_set:
	
			print "%s(%s)" % (depend_lib,depend_lib_symbol_hash[depend_lib]);
			
		print '=======================\n\n'		
		
	
if __name__ == "__main__":

	PRJ_PATH = sys.argv[1];

	#find all the libs under the directory

	lib_name_array = [];

	for(dirpath,dirnames,filenames) in os.walk(PRJ_PATH):

		lib_pattern = re.compile(r'\.a$');
	
		for filename in filenames:
	
			if not lib_pattern.search(filename):
		
				continue;
		
			file_path = os.path.join(dirpath,filename);
		
			lib_name_array.append(file_path);
	
	#call the findDependency function
	
	findDependency(lib_name_array);
	
					
	