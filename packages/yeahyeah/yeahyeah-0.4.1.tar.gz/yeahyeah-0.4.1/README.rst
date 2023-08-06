========
yeahyeah
========

.. image:: https://img.shields.io/travis/sjoerdk/yeahyeah.svg
        :target: https://travis-ci.org/sjoerdk/yeahyeah

.. image:: https://readthedocs.org/projects/yeahyeah/badge/?version=latest
        :target: https://yeahyeah.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/sjoerdk/yeahyeah/shield.svg
     :target: https://pyup.io/repos/github/sjoerdk/yeahyeah/
     :alt: Updates

.. image:: https://codecov.io/gh/sjoerdk/yeahyeah/branch/master/graph/badge.svg
     :target: https://codecov.io/gh/sjoerdk/yeahyeah



CLI launch manager. Dispense with the 5 manual steps for everything, just say yeah yeah I know just do it come on move


* Free software: MIT license
* Documentation: https://yeahyeah.readthedocs.io.

What
----
With yeahyeah you can, for example, do this in a console window::

    $ jj virus
    > launches www.virustotal.com

    $ jj search a website
    > searches for 'a website' on duckduckgo

    $ jj admin url_pattern add 'wikipedia' https://wikipedia.org
    > adds an item 'wikipedia' that launches the given url

    $ jj w<tab>
    website   wikipedia
    $ jj wi<tab>
    $ jj wikipedia
    > tab completion on all items

    $ jj my_folder          # launches a set path in new terminal window

    $ jj log add writing    # adds a log message 'writing' to clockifiy


Features
--------

* Launch commands from console/terminal
* Command line interface based on python Click
* Autocomplete for bash and zsh
* Plugin architecture. Write your own
* Wildcard commands like 'Open firefox search on search term X'


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
