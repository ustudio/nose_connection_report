#!/usr/bin/env python

from setuptools import setup

setup(
    name="nose_connection_report",
    version="0.2",

    description = "Nose testing framework plugin for monitoring network connections",
    author = "Thomas Stephens, John J. Lee, Dan McCombs",
    author_email = "thomas@ustudio.com",
    license = "BSD",
    platforms = ["any"],

    install_requires = ["nose>=0.1.0, ==dev"],

    url = "http://github.com/ustudio/nose_connection_report/",

    long_description = """\
Plugin for the nose testing framework for monitoring network connections during test

Use ``nosetests --with-connection-report`` to enable the plugin.  When enabled,
each test is run in a separate process.

Supports Python 2 and 3.
""",

    py_modules = ["nose_connection_report"],
    entry_points = {
        "nose.plugins.0.10": [
            "connection-report = nose_connection_report:ConnectionReportPlugin",
            "process-isolation-reporter = "
                "nose_connection_report:ProcessIsolationReporterPlugin"]
        },
    zip_safe = True,
)
