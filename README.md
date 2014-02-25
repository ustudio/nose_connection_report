[![Build Status](https://travis-ci.org/ustudio/nose_connection_report.png?branch=master)](https://travis-ci.org/ustudio/nose_connection_report)

Nose Connection Report
========

Nose Connection Report is a nose plugin which runs each test in a
subprocess through strace, and monitors network connections made
during each test. It can be used to identify tests which talk to
external services

Nose Connection Report is forked from Nosepipe, which was originally
written by John J. Lee <jjl@pobox.com> and updated by Dan McCombs
<dmccombs@dyn.com> to support newer Python versions.

It's available under the BSD license.

Installing
========

You can install via pip by running:

pip install nose-connection-report

You can install the latest git version by cloning the repository and running:

python ./setup.py install

Usage
========

To use Nose Connection Report, simply add --with-connection-report to
your nosetests command.  When enabled, each test is run *very slowly*
in a separate process.

You can filter out specific connections by adding
`--connection-report-ignore ipaddr:port`. If you need to filter
multiple IP/port combinations, you need to specify
`--connection-report-ignore` multiple times (due to a limitation in
the legacy `optparse` module used by nose)
