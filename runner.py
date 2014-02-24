#! bin/python
# This lets you run tests during development without installing the
# package using setuptools. It's only necessary for development
# purposes.

import nose
from nose_connection_report import ConnectionReportPlugin

if __name__ == "__main__":
    nose.main(addplugins=[ConnectionReportPlugin()])
