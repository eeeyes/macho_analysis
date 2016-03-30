# -*- coding: utf-8 -*-

import re;

import os;

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
	
# Path: /Users/chaoran/Library/Developer/Xcode/DerivedData/QiYiVideo-cblgmmoeleimbphjbcmsbzrcwhle/Build/Intermediates/ArchiveIntermediates/QiYiVideo/IntermediateBuildFilesPath/QiYiVideo.build/Release-iphoneos/QiYiVideo.build/Objects-normal/armv7/iQiYiPhoneVideo
# Arch: armv7
# Object files:
#.....
# Sections:
# Address	Size    	Segment	Section
#.....
# Symbols:
# Address	Size    	File  Name

class LinkMapParser:

	LINKMAP_STATE_NONE = 0;

	LINKMAP_STATE_PATH = 1;

	LINKMAP_STATE_ARCH = 2;

	LINKMAP_STATE_OBJS = 3;

	LINKMAP_STATE_SECTS = 4;

	LINKMAP_STATE_SECTS_ADDRESS = 5;

	LINKMAP_STATE_SYMBOLS = 6;

	LINKMAP_STATE_SYMBOLS_ADDRESS = 7;

	def __init__(self,linkfile_path):
	
		self.link_file = open(linkfile_path);
		
		self.current_state = LinkMapParser.LINKMAP_STATE_NONE;
		
		self.obj_hash = dict();
		
		self.address_item_array = [];
		
	def parse(self):
	
		for line in self.link_file:

			line = line.strip();
	
			need_next_line,self.current_state = self.linkmapNewState(self.current_state,line);
	
			if need_next_line:
	
				continue;
	
			self.linkmapHandleState(line);
	
	def cleanup(self):
	
		self.link_file.close();
	
	def linkmapHandleState(self,line):

		if self.current_state == LinkMapParser.LINKMAP_STATE_OBJS:
		
			object_pattern = re.compile(r'\[([\s|\d]+)\]\s+(.+)$',re.I);
			
			obj_match = object_pattern.search(line);
		
			obj_num = int(obj_match.groups()[0]);
		
			obj_path = obj_match.groups()[1];
			
			#print obj_num;print obj_path;
			
			self.obj_hash[obj_num] = obj_path;
			
			return;
		
		if self.current_state == LinkMapParser.LINKMAP_STATE_SYMBOLS_ADDRESS:
		
			#print line;
			
			address_pattern = re.compile(r'(\S+)\s+(\S+)\s+\[([\s|\d]+)\]');
			
			symbol_match = address_pattern.search(line);
			
			if not symbol_match:
			
				return;
				
			address = int(symbol_match.groups()[0],16);
			
			size = int(symbol_match.groups()[1],16);
			
			obj_idx = int(symbol_match.groups()[2]);
			
			self.address_item_array.append((address,address+size-1,obj_idx));
			#print address;print size;print obj_idx;
		
			return;
		 
	def linkmapNewState(self,current_state,line):

		if current_state == LinkMapParser.LINKMAP_STATE_NONE:
		
			path_state_pattern = re.compile(r'^#\s+path',re.I);
		
			if path_state_pattern.search(line):
		
				return (1,LinkMapParser.LINKMAP_STATE_PATH);
	
			raise 'PARSE LINKMAP ERROR!!!';
		
		if current_state == LinkMapParser.LINKMAP_STATE_PATH:
	
			arch_state_pattern = re.compile(r'^#\s+arch',re.I);
		
			if arch_state_pattern.search(line):
		
				return (1,LinkMapParser.LINKMAP_STATE_ARCH);
			
			raise 'PARSE LINKMAP ERROR'
		
		if current_state == LinkMapParser.LINKMAP_STATE_ARCH:
	
			objs_state_pattern = re.compile(r'^#\s+object\s+files',re.I);
		
			if objs_state_pattern.search(line):
		
				return (1,LinkMapParser.LINKMAP_STATE_OBJS);
			
			raise 'PARSE LINKMAP ERROR';
		
		if current_state == LinkMapParser.LINKMAP_STATE_OBJS:
	
			sections_state_pattern = re.compile(r'^#\s+sections',re.I);
		
			if sections_state_pattern.search(line):
		
				return (1,LinkMapParser.LINKMAP_STATE_SECTS);
			
			return (0,LinkMapParser.LINKMAP_STATE_OBJS);
		
		if current_state == LinkMapParser.LINKMAP_STATE_SECTS:
	
			sections_address_state_pattern = re.compile(r'^#\s+address',re.I);
		
			if sections_address_state_pattern.search(line):
		
				return (1,LinkMapParser.LINKMAP_STATE_SECTS_ADDRESS);
					
			raise 'PARSE LINKMAP ERROR';
		
		if current_state == LinkMapParser.LINKMAP_STATE_SECTS_ADDRESS:
	
			symbols_state_pattern = re.compile(r'^#\s+symbols',re.I);
		
			if symbols_state_pattern.search(line):
		
				return (1,LinkMapParser.LINKMAP_STATE_SYMBOLS);
			
			return (0,LinkMapParser.LINKMAP_STATE_SECTS_ADDRESS);
		
		if current_state == LinkMapParser.LINKMAP_STATE_SYMBOLS:
	
			symbols_address_state_pattern = re.compile(r'^#\s+address',re.I);
		
			if symbols_address_state_pattern.search(line):
		
				return (1,LinkMapParser.LINKMAP_STATE_SYMBOLS_ADDRESS);
			
			raise 'PARSE LINKMAP ERROR'
		
		if current_state == LinkMapParser.LINKMAP_STATE_SYMBOLS_ADDRESS :
	
			return (0,LinkMapParser.LINKMAP_STATE_SYMBOLS_ADDRESS);
			
		raise 'PARSE LINKMAP ERROR';

def findCallingSymbolModule(symbol,linkmap_path,disassembly_path):

	address_array = parseDisassemblyFile(disassembly_path,symbol);
	
	linkmap_parser = LinkMapParser(linkmap_path);

	linkmap_parser.parse();

	linkmap_parser.cleanup();

	found_address = 0;

	obj_path_set = set();

	for obj_address_item in linkmap_parser.address_item_array:

		start_address = obj_address_item[0];
	
		end_address = obj_address_item[1];
	
		obj_idx = obj_address_item[2];
	
		obj_path = os.path.basename(linkmap_parser.obj_hash[obj_idx]);
	
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