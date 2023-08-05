|License| |Build Status|

Library for quick CLI user prompts, input, and menus.

Introduction
============

This project provides a Python 2.7/3.3+ library that allows the user to
quickly create CLI prompts for user input. The main features of Qprompt
are:

-  Simple multi-entry menus.

-  Prompt for typed (integer/float/string) input.

-  Optional default values and validity checks.

-  Various CLI convenience functions.

-  User input can optionally be supplied from script command-line
   arguments allowing for simple automation.

-  Should work on any platform without additional dependencies.

|Demo|

Status
======

Currently, this project is in the **development release** stage. While
this project is suitable for use, please note that there may be
incompatibilities in new releases.

Release notes are maintained in the project
`changelog <https://github.com/jeffrimko/Qprompt/blob/master/CHANGELOG.adoc>`__.

Requirements
============

Qprompt should run on any Python 2.7/3.3+ interpreter and uses some
third-party libraries.

Installation
============

Qprompt is `available on PyPI
here <https://pypi.python.org/pypi/qprompt>`__ and can be installed with
pip using the following command: ``pip install qprompt``

Additionally, Qprompt can be installed from source by running:
``python setup.py install``

Documentation
=============

The full documentation for this project can be found `here on Read the
Docs <http://qprompt.readthedocs.io>`__.

Roadmap
=======

The following potential updates are under consideration:

-  Accept multiple menu choices from user at once; e.g. space separated
   entries like ``1 2 q``.

-  Timeouts for prompt inputs; default value used if timed out.

Contributing
============

Contributions or feedback is welcome and encouraged!

A list of those who have helped with this project is available in the
`authors
file <https://github.com/jeffrimko/Qprompt/blob/master/AUTHORS.adoc>`__.

Similar
=======

The following projects are similar and may be worth checking out:

-  `bullet <https://github.com/Mckinsey666/bullet>`__

-  `cliask <https://github.com/Sleft/cliask>`__

-  `Promptly <https://github.com/aventurella/promptly>`__

-  `python-inquirer <https://github.com/magmax/python-inquirer>`__

-  `python-prompt <https://github.com/sfischer13/python-prompt>`__

-  `python-prompt-toolkit <https://github.com/jonathanslenders/python-prompt-toolkit>`__

-  `prompter <https://github.com/tylerdave/prompter>`__

.. |Qprompt| image:: doc/logo/qprompt.png
.. |License| image:: http://img.shields.io/:license-mit-blue.svg
.. |Build Status| image:: https://travis-ci.org/jeffrimko/Qprompt.svg?branch=master
.. |Demo| image:: https://raw.githubusercontent.com/jeffrimko/Qprompt/master/doc/demos/main_demo.gif

