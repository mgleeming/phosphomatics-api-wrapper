Introduction
============

Phosphomatics is a public resource for statistical and downstream analysis of phosphoproteomics data. The graphical web resource can be accessed `here <https://www.phosphomatics.com>`_. A limited API is available that allows users to automate the process of uploading and initial data processing. Here, we provide a python wrapper to this API.

This is very much a work in progress so use at your own risk.

Installation
---------------

Create a virtual environment::

    virtualenv venv
    source venv/bin/activate

Either install from PyPi::

    pip install phosphomatics-api-wrapper

Or clone the GitHub repo and install manually::

    git clone https://github.com/mgleeming/phosphomatics-api-wrapper.git
    cd phosphomatics-api-wrapper
    pip install -r requirements.txt
    python setup.py install

API Keys
--------

A unique key is required to use the phosphomatics API. To obtain an API key, contact the devlopers.
