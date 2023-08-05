from distutils.core import setup
setup(
  name = 'LibSerial25',       
  packages = ['LibSerial25'],   
  version = '0.1',      
  license='MIT',       
  description = 'Biblioteca LibSerial25 ',   
  author = 'Walber Hugo',                  
  author_email = 'walberhugo07@hotmail.com',     
  url = 'https://github.com/headllama/LibSerial25',  
  download_url = 'https://github.com/path/LibSerial25/archive/0.1.tar.gz',    
  keywords = ['Serial', 'Senai', 'ComPort'],  
  install_requires=[           
          'datetime',
          'random',         
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
