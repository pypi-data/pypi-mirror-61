# Document Polluter

## Overview

Document Polluter replaces gendered words in documents to create test data for machine learning models in order to identify bias.

Checkout the examples in the [interactive notebook](https://mybinder.org/v2/gh/gregology/document-polluter/notebook).

## Installation

`document-polluter` is available on PyPI

http://pypi.python.org/pypi/document-polluter

### Install via pip

`$ pip install document-polluter`

### Install via easy_install

`$ easy_install document-polluter`

### Install from repo

`git repo <https://github.com/gregology/document-polluter>`

```
$ git clone --recursive git://github.com/gregology/document-polluter.git
$ cd document-polluter
$ python setup.py install
```

## Basic usage

```
>>> from document_polluter import DocumentPolluter
>>> documents = ['she shouted', 'my son', 'the parent']
>>> dp = DocumentPolluter(documents=documents, genre='gender')
>>> print(dp.polluted_documents['female'])
['she shouted', 'my daughter', 'the mother']
```

## Running Test

`$ python document_polluter/tests.py `
