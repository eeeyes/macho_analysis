import setuptools;

setuptools.setup(name="macho_analysis",
			
			version="0.01",
			
			description="some utils to help analysis macho files,include util to find which module call the symbol and the dependencies between the modules",
			
			author="chaoran zhang",
			
			author_email="en756303625@163.com",
			
			license='MIT',
			
			packages=['macho_analysis','macho_analysis/utils'],
			
			zip_safe=False);
			
			