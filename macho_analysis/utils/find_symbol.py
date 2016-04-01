# -*- coding: utf-8 -*-

import re;

import os;

from .. import linkmap

def parseDisassemblyFile(disassembly_file_path,symbol):

	disassembly_file = open(disassembly_file_path,'r');

	symbol_pattern = re.compile(re.escape(symbol));
	
	address_pattern = re.compile(r'^(\S+)');

	address_array = [];

	for line in disassembly_file:

		line = line.strip();
	
		if not symbol_pattern.search(line):	

			continue;
	
		address_match = address_pattern.search(line);
	
		address = address_match.groups()[0];
		
		address_array.append(int(address,16));
	
	disassembly_file.close();

	return address_array;
	
def findCallingSymbolModule(symbol,linkmap_path,disassembly_path):

	address_array = parseDisassemblyFile(disassembly_path,symbol);
	
	linkmap_parser = linkmap.Linkmap(linkmap_path);

	linkmap_parser.parse();

	linkmap_parser.cleanup();

	found_address = 0;

	obj_path_set = set();

	for obj_item in linkmap_parser.symbols:

		start_address = obj_item.address;
	
		end_address = obj_item.size + start_address - 1;
	
		#obj_idx = obj_address_item[2];
	
		obj_path = os.path.basename(obj_item.file);
	
		for call_address in address_array:
	
			if call_address <= end_address and call_address >= start_address:
		
				found_address = found_address + 1;
			
				obj_path_set.add(obj_path);
	
	return obj_path_set;
	
	
if __name__ == "__main__":
	
	obj_path_array = [ x for x in findCallingSymbolModule("_NSLog","iQiYiPhoneVideo-LinkMap-normal-armv7.txt","assembly.txt")];

	obj_path_array.sort();

	for obj_path in obj_path_array:

		print obj_path;			