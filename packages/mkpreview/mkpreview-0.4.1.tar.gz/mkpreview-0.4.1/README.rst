==================
mkpreview
==================


.. image:: https://img.shields.io/github/v/release/:cbitterfield/:mkpreview?sort=semver
        :target: https://pypi.org/project/mkpreview/

.. image:: https://img.shields.io/travis/fgriberi/python_boilerplate.svg
        :target: https://travis-ci.org/cbitterfield/mkpreview

.. image:: https://readthedocs.org/projects/mkpreview/badge/?version=latest
        :target: https://mkpreview.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/mkpreview?style=plastic
        :target: https://pypi.org/project/mkpreview/

mkpreview builds a grid of images from a movie file.
- Support for all video file types in FFMPEG.
- It will create a SQLite3 database with all of the video meta dataparameters and create an MD5 hash of the file
- It provides very basic support for creating video part numbers



Get Started!
------------
Here’s how to set up *mkpreview* for local environment.

1- Clone the *mkpreview* locally:

.. code-block:: console

    $ git clone git@github.com:/mkpreview.git

2- Install your local copy into a *virtualenv*. Assuming you have *virtualenvwrapper* installed, this is how you set up the package for local development:

.. code-block:: console

    $ sudo make boostrap
    $ mkvirtualenv mkpreview
    $ pip install -r requirements/dev.txt

3- How to enable/disable virtualenv

.. code-block:: console

    $ workon mkpreview
    $ ...
    $ deactivate


Credits
-------

This package was generated using Yeoman_ and Cookiecutter_ projects.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _Yeoman: https://yeoman.io/learning/
