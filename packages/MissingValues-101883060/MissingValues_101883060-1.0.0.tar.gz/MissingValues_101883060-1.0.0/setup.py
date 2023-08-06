# -*- coding: utf-8 -*-
"""
Created on Sun Feb 09 17:43:51 2020

@author: Rohan Bawa
"""
import setuptools
from distutils.core import setup
setup(
  name='MissingValues_101883060',
  packages = ['MissingValues_101883060'],   # Chose the same as "name"
  version = '1.0.0',      # Start with a small number and increase it with every change you make
  license='MIT',
  description = 'Missing values replacement with mean',
  entry_points ={ 
    'console_scripts': [ 
        'missingval = MissingValues_101883060.missingval:main'
    ] 
  }, 
  long_description_content_type="text/markdown",
  author = 'Rohan Bawa',                   # Type in your name
  keywords = ['nan removal'],   # Keywords that define your package best
  install_requires=[            
          'numpy',
          'pandas'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.6',
    
  ],
)

