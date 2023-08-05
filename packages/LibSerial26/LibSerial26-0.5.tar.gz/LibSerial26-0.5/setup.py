from distutils.core import setup
import setuptools
setup(
  name = 'LibSerial26',
  packages = ['LibSerial26'],
  version = '0.5',
  license='MIT',
  description = 'Biblioteca LibSerial26',
  author = 'Henrique Reno Sawada',
  author_email = 'renohh@gmail.com',
  url = 'https://github.com/renoh/LibSerial26',
  download_url = 'https://github.com/renoh/LibSerial26/archive/0.3.tar.gz',
  keywords = ['Serial', 'SENAI', 'COMPort'],
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
    'Programming Language :: Python :: 3.8',
  ],
)