"""syphon.tests.common.test_readerror.py

   Copyright (c) 2017-2018 Keithley Instruments, LLC.
   Licensed under MIT (https://github.com/ehall/syphon/blob/master/LICENSE)

"""
from syphon.common import ReadError

class TestReadError(object):
    def test_is_exception(self):
        read_error = ReadError('')
        assert isinstance(read_error, Exception)

    def test_single_quote_message_storage(self):
        msg = '"This" is a \'test.\''
        read_error = ReadError(msg)
        assert read_error.message == msg

    def test_double_quote_message_storage(self):
        msg = "\"This\" is a 'test.'"
        read_error = ReadError(msg)
        assert read_error.message == msg

    def test_triple_single_quote_message_storage(self):
        msg = '''"This"
is
a
\'test.\''''
        read_error = ReadError(msg)
        assert read_error.message == msg

    def test_triple_double_quote_message_storage(self):
        msg = """\"This\"
is
a
'test.'"""
        read_error = ReadError(msg)
        assert read_error.message == msg
