import setuptools;

def readme():
    with open('readme.rst') as f:
        return f.read()
        
setuptools.setup(name="macho_analysis",
			
			version="0.011",
			
			description="some utils to help analysis macho files,include util to find which module call the symbol and the dependencies between the modules",
			
			long_description=readme(),
			
			author="chaoran zhang",
			
			keywords='macho analysis symbol module dependencies',
			
			url='https://github.com/eeeyes/macho_analysis.git',
			
			classifiers=[
			
        		'Development Status :: 3 - Alpha',
        	
        		'Operating System :: MacOS :: MacOS X',
        		
        		'License :: OSI Approved :: MIT License',
        	
        		'Programming Language :: Python :: 2.7',
        		
        		'Topic :: Utilities'
        	
      		],
      		
			author_email="en756303625@163.com",
			
			license='MIT',
			
			packages=['macho_analysis','macho_analysis/utils'],
			
			include_package_data=True,
			
			zip_safe=False);
			
			