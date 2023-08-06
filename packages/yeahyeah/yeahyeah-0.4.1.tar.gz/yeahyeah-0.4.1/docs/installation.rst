.. highlight:: shell

============
Installation
============


Stable release
--------------

To install yeahyeah, run this command in your terminal:

.. code-block:: console

    $ pip install yeahyeah

This is the preferred method to install yeahyeah, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Enable autocompletion (linux only)
----------------------------------

After installation type

.. code-block:: console

    $ jj admin enable-autocompletion

for instructions on enabling bash tab-autocompletion for all commands


Window raising
--------------

For linking shortcut keys to raising particular windows, please use https://github.com/MrApplejuice/X11-window-scripts

Integration into UI
-------------------
yeahyeah is a console program, but to make it useful you probably want to integrate it into your window manager
using some shortcut key.

There is no nice installer yet. Only silly lists. Sorry.

Installation and integration (tested on Kubuntu 18.04 only):

- Install yeahyeah: https://yeahyeah.readthedocs.io
- Enable yeahyeah autocompletion: type 'jj anon enable-autocompletion' for instructions
- clone the yeahyeah repo (see below)
- sudo run the file 'scripts/linux/install_yeahyeah_launch.sh
- Make sure xdotool is installed. Can be installed with `sudo apt install xdotool`
- Create a konsole profile named 'yeahyeah' and make any changes you want to it. For example color scheme/ title
- Create a keyboard shortcut to launch the script 'yeahyeah_launch'


From sources
------------

The sources for yeahyeah can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/sjoerdk/yeahyeah

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/sjoerdk/yeahyeah/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install

.. _Github repo: https://github.com/sjoerdk/yeahyeah
.. _tarball: https://github.com/sjoerdk/yeahyeah/tarball/master

