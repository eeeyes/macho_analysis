# -*- coding: utf-8 -*-

import subprocess;

import re;

import os;

import sys;

#first,we should find where is the nm utils

xcode_install_path = subprocess.Popen(['xcode-select','--print-path'],stdout=subprocess.PIPE).communicate()[0].strip();

NM_PATH = os.path.join(xcode_install_path,'Toolchains/XcodeDefault.xctoolchain/usr/bin/nm');
		
class MachoProduct:

	def __init__(self,lib_path,arch):
	
		self.lib_path = lib_path;
		
		self.arch = arch;
		
	def allUndefinedSymbols(self):
	
		nm_cmd = [NM_PATH,'-arch',self.arch,'-u',self.lib_path];

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
			
		nm_cmd = [NM_PATH,'-arch',self.arch,'-U',self.lib_path];

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

def findDependency(lib_path_array,arch):

	lib_symbol_array = [];
	
	#get symbols from libs
	
	for lib_path in lib_path_array:
	
		lib_name = os.path.basename(lib_path);
		
		macho_product = MachoProduct(lib_path,arch);
		
		defined_symbols = macho_product.allDefinedSymbols();
	
		un_defined_symbols = macho_product.allUndefinedSymbols();
	
		lib_symbol_array.append((lib_name,defined_symbols,un_defined_symbols));
		
	
	lib_dep_hash = dict();
	
	#travel all the undefined symbols
			
	for (lib_name,defined_symbols,undefined_symbols) in lib_symbol_array:

		symbol_dep_hash = dict();
		
		lib_dep_hash[lib_name] = symbol_dep_hash;
		
		for undefined_symbol in undefined_symbols:
	
			for (a_lib_name,a_defined_symbols,_) in lib_symbol_array:
		
				if lib_name == a_lib_name:
			
					continue;
				
				if undefined_symbol in a_defined_symbols:
			
					symbol_dep_hash[undefined_symbol]=a_lib_name
				
					break;			
		
	return lib_dep_hash;
	
if __name__ == "__main__":

	PRJ_PATH = sys.argv[1];

	#find all the libs under the project directory

	lib_name_array = [];

	for(dirpath,dirnames,filenames) in os.walk(PRJ_PATH):

		lib_pattern = re.compile(r'\.a$');
	
		for filename in filenames:
	
			if not lib_pattern.search(filename):
		
				continue;
		
			file_path = os.path.join(dirpath,filename);
		
			lib_name_array.append(file_path);
	
	#call the findDependency function
	
	lib_dep_hash = findDependency(lib_name_array,'armv7');
	
	for(lib_name,symbol_dep_hash) in lib_dep_hash.items():
	
		print lib_name;
		
		print '===============';
		
		for (symbol_name,dep_lib) in symbol_dep_hash.items():
		
			print "%s : %s" % (symbol_name,dep_lib);
			
		print '===============';					
	