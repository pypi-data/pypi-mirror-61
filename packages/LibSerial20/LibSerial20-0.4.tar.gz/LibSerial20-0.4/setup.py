from distutils.core import setup
import setuptools
setup(
  name = 'LibSerial20',       
  packages = ['LibSerial20'],   
  version = '0.4',      
  license='MIT',       
  description = 'Biblioteca LibSerial20 ',   
  author = 'Wesley',                  
  author_email = 'diviwfel@gmail.com',     
  url = 'https://github.com/DiviKnight/LibSerial20',  
  download_url = 'https://github.com/DiviKnight/LibSerial20/archive/0.4.tar.gz',    
  keywords = ['Serial', 'Senai', 'ComPort'],  
  install_requires=[           
    'datetime',       
  ],
  classifiers=[
    #"3 - Alpha", "4 - Beta" or "5 - Production/Stable"   
    'Development Status :: 5 - Production/Stable',   
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
  ],
)