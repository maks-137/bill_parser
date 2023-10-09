from setuptools import setup, find_packages

requires=[
  	'beautifulsoup4==4.12.2',
  	'certifi==2023.7.22',
  	'charset-normalizer==3.3.0',
  	'et-xmlfile==1.1.0',
  	'fake-useragent==1.3.0',
  	'idna==3.4',
  	'importlib-resources==6.1.0',
	'lxml==4.9.3',
  	'openpyxl==3.1.2',
  	'PyQt5==5.15.9',
  	'PyQt5-Qt5==5.15.2',
  	'PyQt5-sip==12.12.2',
  	'requests==2.31.0',
  	'soupsieve==2.5',
	'urllib3==2.0.6',
	'zipp==3.17.0',
    ]



setup(
    name='bill-parser',
    version='1.0.0',
    author='Maksym Remezovskyi',
    author_email='maks.remezovskij1@gmail.com',
    description=("bill-parser is a GUI application that allows you to scrape information about bills from " 
		"https://itd.rada.gov.ua/billInfo web-site "
		"according to given filters."),
    url='https://github.com/maks-137/bill_parser',
    packages=find_packages(),
    install_requires=requires,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)