
This package helps in rectifying the spelling of the word with the custom collection of words.

Python Custom Spell Rectify
---------------------------

This package helps in rectifying the spelling of the word with the custom collection of words.
This uses numpy and difflib module.

Installation
------------

You can install directly after cloning:

use the Python package:

.. code-block:: bash

  $ pip install --user py_custom_spellrectify

Command line tool
-----------------

After installation, you should have ``py_custom_spellrectify`` in your ``$PATH``:


Usage
-----

Initailize the handler and load the custom list and auto correct:

.. code-block:: python

    >>> from py_custom_spellrectify import WordCorrection
    >>> word_handler= WordCorrection()
    >>> word_handler.load(input_words=['Commercially', 'available', 'development', 'Discontinued', 'Production', 'Ready', 'Samples', 'Prototype'])
    >>> result= word_handler.correct(input='develop', threshold=0.75)
    >>> print(result)
    >>> ('development', 0.78)


For words whose macthing percentage is lesser than threshold:

.. code-block:: python

    >>> result= word_handler.correct(input='devel', threshold=0.75)
    >>> print(result)
    >>> devel
    >>> # the above will return the same input word if the word if the mataching percentage is lesser than the threshold.



License
~~~~~~~
MIT License
~~~~~~~~~~~


.. code:: rst

    |MIT license|

    .. image:: https://img.shields.io/badge/License-MIT-blue.svg


Contact
~~~~~~~
Please submit an issue if you encounter a bug and please email any questions or requests to
1. vimald8959@gmail.com ( https://github.com/vimal-dharmalingam )
2. catchmaurya@gmail.com ( https://github.com/catchmaurya )