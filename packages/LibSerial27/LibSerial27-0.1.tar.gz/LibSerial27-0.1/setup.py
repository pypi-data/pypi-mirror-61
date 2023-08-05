from distutils.core import setup
setup(
  name = 'LibSerial27',       
  packages = ['LibSerial27'],   
  version = '0.1',      
  license='MIT',       
  description = 'Biblioteca LibSerial27 ',   
  author = 'Nome do Autor',                  
  author_email = 'Email@gmail.com',     
  url = 'https://github.com/AntonioBeneditouol/AntonioBenedito/blob/master/LibSerial27.py',
  download_url = 'https://github.com/AntonioBeneditouol/AntonioBenedito/archive/0.1.tar.gz',    
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