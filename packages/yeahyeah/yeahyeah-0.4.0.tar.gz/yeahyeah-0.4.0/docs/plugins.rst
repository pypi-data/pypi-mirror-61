.. highlight:: shell

===================
Plugin Installation
===================

* pip install <yeahyeah_plugin>  (see below for available plugins)

* Add the plugin to yeahyeah::

    $ jj admin yeahyeah edit-plugins

This will open the list in a standard editor. Add the python import path to the plugin here. For detailed instructions
see the list below


List of plugins
===============

* The `yeahyeah_ad_plugin`_ adds functions to query active directory
* The `yeahyeah_clockify_plugin`_ Allows writing of log messages, starting stopping timer from the console
* The `yeahyeah_path_item_plugin`_ Allows opening of new console windows on pre-defined locations

.. _yeahyeah_ad_plugin: https://github.com/sjoerdk/yeahyeah_ad_plugin
.. _yeahyeah_clockify_plugin: https://github.com/sjoerdk/yeahyeah/tree/master/yeahyeah_plugins/clockify_plugin
.. _yeahyeah_path_item_plugin: https://github.com/sjoerdk/yeahyeah/tree/master/yeahyeah_plugins/path_item_plugin