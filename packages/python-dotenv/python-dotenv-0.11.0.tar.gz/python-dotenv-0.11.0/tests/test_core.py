# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import contextlib
import os
import sys
import textwrap

import logging
import mock
import pytest
import sh

from dotenv import dotenv_values, find_dotenv, load_dotenv, set_key
from dotenv.compat import PY2, StringIO


@contextlib.contextmanager
def restore_os_environ():
    environ = dict(os.environ)

    try:
        yield
    finally:
        os.environ.update(environ)


def test_warns_if_file_does_not_exist():
    logger = logging.getLogger("dotenv.main")

    with mock.patch.object(logger, "warning") as mock_warning:
        load_dotenv('.does_not_exist', verbose=True)

    mock_warning.assert_called_once_with("File doesn't exist %s", ".does_not_exist")


def test_find_dotenv(tmp_path):
    """
    Create a temporary folder structure like the following:

        test_find_dotenv0/
        └── child1
            ├── child2
            │   └── child3
            │       └── child4
            └── .env

    Then try to automatically `find_dotenv` starting in `child4`
    """

    curr_dir = tmp_path
    dirs = []
    for f in ['child1', 'child2', 'child3', 'child4']:
        curr_dir /= f
        dirs.append(curr_dir)
        curr_dir.mkdir()

    child1, child4 = dirs[0], dirs[-1]

    # change the working directory for testing
    os.chdir(str(child4))

    # try without a .env file and force error
    with pytest.raises(IOError):
        find_dotenv(raise_error_if_not_found=True, usecwd=True)

    # try without a .env file and fail silently
    assert find_dotenv(usecwd=True) == ''

    # now place a .env file a few levels up and make sure it's found
    dotenv_file = child1 / '.env'
    dotenv_file.write_bytes(b"TEST=test\n")
    assert find_dotenv(usecwd=True) == str(dotenv_file)


def test_load_dotenv(tmp_path):
    os.chdir(str(tmp_path))
    dotenv_path = '.test_load_dotenv'
    sh.touch(dotenv_path)
    set_key(dotenv_path, 'DOTENV', 'WORKS')
    assert 'DOTENV' not in os.environ
    success = load_dotenv(dotenv_path)
    assert success
    assert 'DOTENV' in os.environ
    assert os.environ['DOTENV'] == 'WORKS'


def test_load_dotenv_override(tmp_path):
    os.chdir(str(tmp_path))
    dotenv_path = '.test_load_dotenv_override'
    key_name = "DOTENV_OVER"
    sh.touch(dotenv_path)
    os.environ[key_name] = "OVERRIDE"
    set_key(dotenv_path, key_name, 'WORKS')
    success = load_dotenv(dotenv_path, override=True)
    assert success
    assert key_name in os.environ
    assert os.environ[key_name] == 'WORKS'


def test_load_dotenv_in_current_dir(tmp_path):
    dotenv_path = tmp_path / '.env'
    dotenv_path.write_bytes(b'a=b')
    code_path = tmp_path / 'code.py'
    code_path.write_text(textwrap.dedent("""
        import dotenv
        import os

        dotenv.load_dotenv(verbose=True)
        print(os.environ['a'])
    """))
    os.chdir(str(tmp_path))

    result = sh.Command(sys.executable)(code_path)

    assert result == 'b\n'


def test_ipython(tmp_path):
    from IPython.terminal.embed import InteractiveShellEmbed
    os.chdir(str(tmp_path))
    dotenv_file = tmp_path / '.env'
    dotenv_file.write_text("MYNEWVALUE=q1w2e3\n")
    ipshell = InteractiveShellEmbed()
    ipshell.magic("load_ext dotenv")
    ipshell.magic("dotenv")
    assert os.environ["MYNEWVALUE"] == 'q1w2e3'


def test_ipython_override(tmp_path):
    from IPython.terminal.embed import InteractiveShellEmbed
    os.chdir(str(tmp_path))
    dotenv_file = tmp_path / '.env'
    os.environ["MYNEWVALUE"] = "OVERRIDE"
    dotenv_file.write_text("MYNEWVALUE=q1w2e3\n")
    ipshell = InteractiveShellEmbed()
    ipshell.magic("load_ext dotenv")
    ipshell.magic("dotenv -o")
    assert os.environ["MYNEWVALUE"] == 'q1w2e3'


def test_dotenv_values_stream():
    stream = StringIO(u'hello="it works!😃"\nDOTENV=${hello}\n')
    stream.seek(0)
    parsed_dict = dotenv_values(stream=stream)
    assert 'DOTENV' in parsed_dict
    assert parsed_dict['DOTENV'] == u'it works!😃'


def test_dotenv_values_no_interpolate():
    stream = StringIO(u'no_interpolate=$MYVAR')
    stream.seek(0)
    parsed_dict = dotenv_values(stream=stream, interpolate=False)
    assert 'no_interpolate' in parsed_dict
    assert parsed_dict['no_interpolate'] == u'$MYVAR'


def test_dotenv_values_no_interpolate_strict():
    stream = StringIO(u'no_interpolate_strict=${MYVAR}')
    stream.seek(0)
    parsed_dict = dotenv_values(stream=stream, interpolate=False)
    assert 'no_interpolate_strict' in parsed_dict
    assert parsed_dict['no_interpolate_strict'] == u'${MYVAR}'


def test_dotenv_values_export():
    stream = StringIO('export foo=bar\n')
    stream.seek(0)
    load_dotenv(stream=stream)
    assert 'foo' in os.environ
    assert os.environ['foo'] == 'bar'


def test_dotenv_values_utf_8():
    stream = StringIO(u"a=à\n")
    load_dotenv(stream=stream)
    if PY2:
        assert os.environ["a"] == u"à".encode(sys.getfilesystemencoding())
    else:
        assert os.environ["a"] == "à"


def test_dotenv_empty_selfreferential_interpolation():
    stream = StringIO(u'some_path="${some_path}:a/b/c"\n')
    stream.seek(0)
    assert u'some_path' not in os.environ
    parsed_dict = dotenv_values(stream=stream)
    assert {u'some_path': u':a/b/c'} == parsed_dict


def test_dotenv_nonempty_selfreferential_interpolation():
    stream = StringIO(u'some_path="${some_path}:a/b/c"\n')
    stream.seek(0)
    assert u'some_path' not in os.environ
    with restore_os_environ():
        os.environ[u'some_path'] = u'x/y/z'
        parsed_dict = dotenv_values(stream=stream)
    assert {u'some_path': u'x/y/z:a/b/c'} == parsed_dict
