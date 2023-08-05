================
django-textrank
================

It is simple web-service for ranging a text by keywords.

Installation
------------

.. code-block:: shell

    pip3 install django-textrank
    # or
    pip3 install git+https://gitlab.com/djbaldey/django-textrank.git@master#egg=django-textrank


Quick start
-----------

1. Add "textrank" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'djangokit',
        'textrank',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('textrank/', include('textrank.urls')),

3. Run `python3 manage.py migrate` to create the necessary models.

4. Start the development server and visit http://127.0.0.1:8000/textrank/
   to check your text.
