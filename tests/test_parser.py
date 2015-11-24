# -*- coding: utf-8 -*-


import pytest

from dotenvfile import loads


def test_valid_envfile():
    lines = loads('\n'.join([
        'FOO=1',
        'BAR=abc',
    ]))
    assert lines == {
        'FOO': '1',
        'BAR': 'abc',
    }


def test_continuing_line():
    lines = loads('\n'.join([
        'FOO=abc\\',
        'def',
        'BAR=hij',
    ]))
    assert lines == {
        'FOO': 'abcdef',
        'BAR': 'hij',
    }


def test_continuing_line_leading_whitespace():
    lines = loads('\n'.join([
        'FOO=abc\\',
        '   def',
        'BAR=hij',
    ]))
    assert lines == {
        'FOO': 'abcdef',
        'BAR': 'hij',
    }


def test_duplicate_variable():
    with pytest.raises(ValueError) as error:
        print(loads('\n'.join([
            'FOO=1',
            'FOO=2',
        ])))
    assert error.value.args[0] == [
        'Line 2: duplicate environment variable "FOO": already appears on line 1.',
    ]
