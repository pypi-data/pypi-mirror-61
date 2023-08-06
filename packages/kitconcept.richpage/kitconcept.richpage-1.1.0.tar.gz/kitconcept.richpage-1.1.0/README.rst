.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
kitconcept.richpage
==============================================================================

.. image:: https://travis-ci.org/kitconcept/kitconcept.richpage.svg?branch=master
    :target: https://travis-ci.org/kitconcept/kitconcept.richpage

.. image:: https://img.shields.io/pypi/status/kitconcept.richpage.svg
    :target: https://pypi.python.org/pypi/kitconcept.richpage/
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/v/kitconcept.richpage.svg
    :target: https://pypi.python.org/pypi/kitconcept.richpage/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/kitconcept.richpage.svg
    :target: https://pypi.python.org/pypi/kitconcept.richpage/
    :alt: License

|

.. image:: https://raw.githubusercontent.com/kitconcept/kitconcept.richpage/master/kitconcept.png
   :alt: kitconcept
   :target: https://kitconcept.com/

|

kitconcept.richpage is a Plone add-on product with a "folderish" RichPage
content object.
A RichPage can contain the following content:

- Text
- Image
- Audio
- Video
- File
- Slideshow
- Google Maps

This package does only contain the bare content types.
You currently have to build your own front-end for this.
We recommend to use plone-react for this.

Features
--------

- Can be bullet points


Examples
--------

This add-on can be seen in action at the following sites:
- Is there a page on the internet where everybody can see the features?


Documentation
-------------

Full documentation for end users can be found in the "docs" folder, and is also available online at http://docs.plone.org/foo/bar


Translations
------------

This product has been translated into

- German


Installation
------------

Install kitconcept.richpage by adding it to your buildout::

    [buildout]

    ...

    eggs =
        kitconcept.richpage


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/kitconcept/kitconcept.richpage/issues
- Source Code: https://github.com/kitconcept/kitconcept.richpage


Support
-------

If you are having issues, please let us know.
Send an email to info@kitconcept.com.

License
-------

The project is licensed under the GPLv2.
