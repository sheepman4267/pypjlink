# -*- coding: utf-8 -*-

import functools

try:
    from unittest import mock
except ImportError:
    import mock

try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO



class MockProjSocket(object):
    """A context manager that mocks socket creation inside projector module
    Read from the mock returns response string passed in constructor.
    Write into the mock appends data in .written string attribute, besides
    calling .write mock method
    """

    mock_target = 'pypjlink.projector.socket.socket'

    def __init__(self, response):
        self._response = response
        self._mock_sock = None

    def __enter__(self):
        mock_socket_func = mock.patch(self.mock_target).__enter__()
        self._mock_sock = mock_socket_func.return_value
        stream = self._mock_sock.makefile.return_value
        buf = StringIO(self._response)
        stream.read = buf.read
        stream.written = ''

        def _write(data):
            stream.written += data
        stream.write.side_effect = _write

        return stream

    def __exit__ (self, exc_type, exc_value, traceback):
        self._mock_sock.__exit__()
