# ofxstatement-zm-stanbic

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Stanbic Zambia plugin for ofxstatement 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This project provides a custom plugin for [ofxstatement](https://github.com/kedder/ofxstatement) for Stanbic Bank (ZM). It is based
on the work done by JBBandos (https://github.com/jbbandos/ofxstatement-be-ing).

`ofxstatement`_ is a tool to convert proprietary bank statement to OFX format, suitable for importing to GnuCash / Odoo. Plugin for ofxstatement parses a particular proprietary bank statement format and produces common data structure, that is then formatted into an OFX file.

Users of ofxstatement have developed several plugins for their banks. They are listed on main [`ofxstatement`](https://github.com/kedder/ofxstatement) site. If your bank is missing, you can develop
your own plugin.

## Installation

### From PyPI repositories
```
pip3 install ofxstatement-zm-stanbic
```

### From source
```
git clone git@github.com:BIZ4Africa/ofxstatement-zm-stanbic.git 
python3 setup.py install
```

## Usage
```
$ ofxstatement convert -t stanbiczm input.csv output.ofx
```
Note: Stanbic does not provide csv export, but this plugin is based on the CSV from PDF using tabula-py module
