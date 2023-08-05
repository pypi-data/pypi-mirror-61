# FollowName

FollowName is a simple implementation of GNU tail --follow=name

It provides an Iterator generator followname that returns lines as data is added to the file.

If the file is truncated or replaced followname will open the new file. 

followname only requires read access to the file.

* ``followname`` - read lines as a file grows

It also comes with ``followname``, a command line version offering the same functionality as GNU tail --follow=name. 

- `FollowName on GitHub <http://github.com/stuartlynne/pyfollowname>`_
- `FollowName on Pypi <http://pypi.python.org/pypi/followname>`_

## Installation

Install with ``pip`` or ``easy_install``.

::

    pip install followname

## Examples

::

    import followname
    follower = FollowName("testfile.txt")
    for line in follower.follow(open('test.txt')):
        print line

## Running Tests

FollowName currently only has doctests.

Run tests with nose::

    nosetests --with-doctest src/followname

Run tests with doctest::

    python -m doctest -v src/followname/__init__.py
