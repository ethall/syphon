"""syphon.tests.test_main.py

   Copyright (c) 2017-2018 Keithley Instruments, LLC.
   Licensed under MIT (https://github.com/ehall/syphon/blob/master/LICENSE)

"""
from syphon.__version__ import __version__
from syphon.__main__ import _main

def test_main_version(capsys):
    arguments = ['syphon', '--version']
    _main(arguments)
    output = capsys.readouterr()
    assert output.out == '{}\n'.format(__version__)
