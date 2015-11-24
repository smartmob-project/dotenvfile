# -*- coding: utf-8 -*-

"""Parser for ``.env`` files.

Implements `Smartmob RFC 2 <http://smartmob-rfc.readthedocs.org/en/latest/2-dotenv.html>`_."""

import re


_ENVFILE_LINE = re.compile(
    ''.join([
        r'^(?P<variable>.+?)=(?P<value>.+)$',
    ])
)


def _find_duplicates(items):
    seen = {}
    duplicates = []
    for i, item in items:
        if item in seen:
            duplicates.append((i, item, seen[item]))
        else:
            seen[item] = i
    return duplicates


def _group_lines(lines):
    start, group = (0, [])
    for i, line in enumerate(lines):
        if line.rstrip().endswith('\\'):
            group.append(line[:-1])
        else:
            if group:
                group.append(line.lstrip())
            else:
                group.append(line)
            yield start, ''.join(group)
            start, group = (i + 1, [])
    if group:
        yield start, ''.join(group[:-1]) + group[-1].rstrip()


def _parse_procfile_line(line):
    line = line.strip()
    match = _PROCFILE_LINE.match(line)
    if match is None:
        raise ValueError('Invalid profile line "%s".' % line)
    parts = match.groupdict()
    environment = parts['environment']
    if environment:
        environment = [
            tuple(variable.strip().split('='))
            for variable in environment.strip().split(' ')
        ]
    else:
        environment = []
    return (
        parts['process_type'],
        parts['command'],
        environment,
    )

def _parse_envfile_line(line):
    line = line.strip()
    match = _ENVFILE_LINE.match(line)
    if match is None:
        raise ValueError('Invalid profile line "%s".' % line)
    parts = match.groupdict()
    return parts['variable'], parts['value']


def loads(content):
    """Loads variable definitions from a string."""
    lines = _group_lines(line for line in content.split('\n'))
    lines = [
        (i, _parse_envfile_line(line))
        for i, line in lines if line.strip()
    ]
    errors = []
    # Reject files with duplicate variables (no sane default).
    duplicates = _find_duplicates(((i, line[0]) for i, line in lines))
    for i, variable, j in duplicates:
        errors.append(''.join([
                'Line %d: duplicate environment variable "%s": ',
                'already appears on line %d.',
            ]) % (i + 1, variable, j + 1)
        )
    # Done!
    if errors:
        raise ValueError(errors)
    return {k: v for _, (k, v) in lines}

def load(stream):
    """Loads variable definitions from a file-like object."""
    return loads(stream.read().decode('utf-8'))

def loadfile(path):
    """Loads variable definitions from a file."""
    with open(path, 'rb') as stream:
        return load(stream)
