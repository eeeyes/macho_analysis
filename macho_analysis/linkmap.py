import re;

class LinkmapSection:

	def __init__(self,address,size,segment,section):
	
		self.address = address;
		
		self.size = size;
		
		self.segment = segment;
		
		self.section = section;
	
class LinkmapSymbol:

	def __init__(self,address,size,file,name):
	
		self.address = address;
		
		self.size = size;
		
		self.file = file;
		
		self.name = name;
			
class Linkmap:

	LINKMAP_STATE_START = 'start';
	
	LINKMAP_STATE_PATH = 'path';
	
	LINKMAP_STATE_ARCH = 'arch';
	
	LINKMAP_STATE_OBJS = 'objs';
	
	LINKMAP_STATE_OBJS_CONTENT = 'objs_content';
	
	LINKMAP_STATE_SECTIONS = 'sections';
	
	LINKMAP_STATE_SECTIONS_ADDRESS = 'sections_address';
	
	LINKMAP_STATE_SECTIONS_CONTENT = 'sections_content';
	
	LINKMAP_STATE_SYMBOLS = 'symbols';
	
	LINKMAP_STATE_SYMBOLS_ADDRESS = 'symbols_address';
	
	LINKMAP_STATE_SYMBOLS_CONTENT = 'symbols_content';
	
	def __init__(self,linkmap_path):
	
		self.linkmap_file = open(linkmap_path);
	
		#map from idx to obj_path
		
		self.objs_hash = dict();
		
		self.sections = [];
		
		self.symbols = [];
		
		self.buildStateChangeTable();
	
	def buildStateChangeTable(self):
	
		self.state_change_table = dict();
		
		self.current_state = self.__class__.LINKMAP_STATE_START;
		
		
		self.path_pattern = re.compile(r'^#\s+Path:\s+(.+)$');
		
		self.arch_pattern = re.compile(r'^#\s+Arch:\s+(.+)$');
	
		self.objs_pattern = re.compile(r'^#\s+Object\s+files:');
		
		self.objs_content_pattern = re.compile(r'\s*\[\s*(\d+)\]\s+(.+)$');
		
		self.sections_pattern = re.compile(r'^#\s*Sections:');
		
		self.sections_address_pattern = re.compile(r'^#(\s*)Address(\s+)Size(\s+)Segment(\s+)Section(\s*)$');
		
		self.sections_content_pattern = re.compile(r'^\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$');
		
		self.symbols_pattern = re.compile(r'^#\s*Symbols:\s*$');
		
		self.symbols_address_pattern = re.compile(r'^#\s*Address\s*Size\s*File\s*Name\s*$');
		
		self.symbols_content_pattern = re.compile(r'^(0x\S+)\s+(0x\S+)\s+\[\s*(\d+)\]\s+(.+)$');
		
		self.anything_pattern = re.compile(r'.*');
		#table[current_state] = [(next_state,next_state_pattern,next_state_handler),...]
		
		self.state_change_table[self.__class__.LINKMAP_STATE_START] = [(self.__class__.LINKMAP_STATE_PATH,self.path_pattern,self.parsePathState)];
		
		self.state_change_table[self.__class__.LINKMAP_STATE_PATH] = [(self.__class__.LINKMAP_STATE_ARCH,self.arch_pattern,self.parseArchState)];
		
		self.state_change_table[self.__class__.LINKMAP_STATE_ARCH] = [(self.__class__.LINKMAP_STATE_OBJS,self.objs_pattern,self.parseObjsState)];
		
		self.state_change_table[self.__class__.LINKMAP_STATE_OBJS] = [(self.__class__.LINKMAP_STATE_OBJS_CONTENT,self.objs_content_pattern,self.parseObjsContentState),
																	(self.__class__.LINKMAP_STATE_SECTIONS,self.sections_pattern,self.parseSectionsState)];
												
																	
		self.state_change_table[self.__class__.LINKMAP_STATE_OBJS_CONTENT] = self.state_change_table[self.__class__.LINKMAP_STATE_OBJS];
		
		self.state_change_table[self.__class__.LINKMAP_STATE_SECTIONS] = [(self.__class__.LINKMAP_STATE_SECTIONS_ADDRESS,self.sections_address_pattern,self.parseSectionsAddressState)];															
		
		self.state_change_table[self.__class__.LINKMAP_STATE_SECTIONS_ADDRESS] = [(self.__class__.LINKMAP_STATE_SECTIONS_CONTENT,self.sections_content_pattern,self.parseSectionsContentState),
																					(self.__class__.LINKMAP_STATE_SYMBOLS,self.symbols_pattern,self.parseSymbolsState)];
																					
		self.state_change_table[self.__class__.LINKMAP_STATE_SECTIONS_CONTENT] = self.state_change_table[self.__class__.LINKMAP_STATE_SECTIONS_ADDRESS];																			
		
		self.state_change_table[self.__class__.LINKMAP_STATE_SYMBOLS] = [(self.__class__.LINKMAP_STATE_SYMBOLS_ADDRESS,self.symbols_address_pattern,self.parseSymbolsAddressState)];
		
		self.state_change_table[self.__class__.LINKMAP_STATE_SYMBOLS_ADDRESS] = [(self.__class__.LINKMAP_STATE_SYMBOLS_CONTENT,self.symbols_content_pattern,self.parseSymbolsContentState)];
		
		self.state_change_table[self.__class__.LINKMAP_STATE_SYMBOLS_CONTENT] = self.state_change_table[self.__class__.LINKMAP_STATE_SYMBOLS_ADDRESS][:];
		
		self.state_change_table[self.__class__.LINKMAP_STATE_SYMBOLS_CONTENT].append((self.__class__.LINKMAP_STATE_SYMBOLS_CONTENT,self.anything_pattern,self.parseAnyThing));
		
	def parsePathState(self,line,match):
	
		self.path = match.groups()[0];
	
		#print self.path;
		
	def parseArchState(self,line,match):
	
		self.arch = match.groups()[0];
		
		#print self.arch;
		
	def parseObjsState(self,line,match):
	
		pass;
		
	def parseObjsContentState(self,line,match):
	
		obj_idx = int(match.groups()[0]);
		
		obj_name = match.groups()[1];
		
		self.objs_hash[obj_idx] = obj_name;
		
		#print obj_idx;print obj_name;
			
	def parseSectionsState(self,line,match):
	
		pass;
		
	def parseSectionsAddressState(self,line,match):
	
		pass;
		
	def parseSectionsContentState(self,line,match):
	
		address = int(match.groups()[0],16);
		
		size = int(match.groups()[1],16);
		
		segment = match.groups()[2];
		
		section = match.groups()[3];
		
		self.sections.append(LinkmapSection(address,size,segment,section));
		
		#print address;print size;print segment;print section;
		
	def parseSymbolsState(self,line,match):
	
		pass;
		
	def parseSymbolsAddressState(self,line,match):
	
		pass;
		
	def parseSymbolsContentState(self,line,match):
	
		address = int(match.groups()[0],16);
		
		size = int(match.groups()[1],16);
		
		#print line;
		
		file_idx = int(match.groups()[2]);
	
		file_name = self.objs_hash[file_idx];
		
		#print file;
			
		name = match.groups()[3];
		
		self.symbols.append(LinkmapSymbol(address,size,file_name,name));
		#print "%s %s %s %s" % (address,size,file,name);
				
	def parseAnyThing(self,line,match):
	
		pass;
		
	# # Path: /Users/chaoran/Library/Developer/Xcode/DerivedData/QiYiVideo-cblgmmoeleimbphjbcmsbzrcwhle/Build/Intermediates/ArchiveIntermediates/QiYiVideo/IntermediateBuildFilesPath/QiYiVideo.build/Release-iphoneos/QiYiVideo.build/Objects-normal/armv7/iQiYiPhoneVideo
	# # Arch: armv7
	# # Object files:
	# ..... 
	#[  0] linker synthesized
	# # Sections:
	# # Address	Size    	Segment	Section
	#.....
	# 0x02B44000	0x00004954	__DATA	__nl_symbol_ptr
	# # Symbols:
	# # Address	Size    	File  Name
	# 0x034DF318	0x00000004	[6586] __ZL9Demangled
	
	def parse(self):
	
		for line in self.linkmap_file:
		
			line = line[:-1];
				
			next_possible_state_array = self.state_change_table[self.current_state];
			
			found_next_state = False;
			
			for (next_state,next_state_pattern,next_state_handler) in next_possible_state_array:
			
				match = next_state_pattern.search(line);
				
				if match:
				
					self.current_state = next_state;
					
					found_next_state = True;
					
					next_state_handler(line,match);
					
					break;
					
			if not found_next_state:
					
				# print '--------';
# 					
# 				print line;print self.current_state;
# 				
# 				print '--------';
				
				raise AssertionError('PARSE ERROR IN THE LINKMAP');
					
	def cleanup(self):
	
		self.linkmap_file.close();	
				
if __name__ == "__main__":

	linkmap = Linkmap("utils/iQiYiPhoneVideo-LinkMap-normal-armv7.txt");
	
	linkmap.parse();
	
	linkmap.cleanup();
	
	pass;	