from distutils.core import setup
setup(
  name = 'LibSerial24',       
  packages = ['LibSerial24'],   
  version = '0.9',      
  license='MIT',       
  description = 'Biblioteca LibSerial24 ',   
  author = 'Isaque Naftali',                  
  author_email = 'isaac.naftali.in@gmail.com',     
  url = 'https://github.com/IsaqueNaftali/Biblioteca_Serial_Python',  
  download_url = 'https://github.com/IsaqueNaftali/Biblioteca_Serial_Python/archive/0.4.tar.gz',    
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