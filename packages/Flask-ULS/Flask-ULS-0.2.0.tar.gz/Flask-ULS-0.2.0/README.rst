Flask-ULS
=========

Integrate the UniversalLanguageSelector_ (ULS) into your Flask application to
allow users to easily change their preferred language in which the application
is rendered. It is recommended to use this in conjunction with localizing your
application.

Usage
-----

In your ``app.py``::

    from flask import Flask
    from flask_uls import ULS

    app = Flask(__name__)
    uls = ULS(app)

You can also use the ``init_app`` pattern as well.

In your template::

    <head>
    {% include 'uls/head.html' %}
    </head>
    <body>
    <span class="uls-trigger">Select language</span>
    {% include 'uls/footer.html' %}
    </body>

This will load the necessary CSS in the header create a button with the text
"Select language" to open up the dialog menu and then load the JavaScript to
configure and trigger ULS.

To integrate ULS with other localization systems, you can access the
``uls.language`` property to get the currently configured language. It will
look at the ``?uselang`` query parameter, the ``language`` cookie (set by ULS
client-side), and the configured default language.

Configuration
-------------

* ``ULS_DEFAULT_LANGUAGE`` (default: ``'en'``): the language to default to if
  the user hasn't selected one.
* ``ULS_ENABLED_LANGUAGES`` (default: ``['en']``): languages that ULS should
  display as options to the user.


Example
-------

See the example_ application which allows users to change their language between
English and German and then outputs the currently chosen language.

License
-------
Flask-ULS is available under the terms of the GPL, version 3 or any later
version.

.. _UniversalLanguageSelector: https://github.com/wikimedia/jquery.uls#universal-language-selector-jquery-library
.. _example: https://git.legoktm.com/legoktm/Flask-ULS/src/master/example