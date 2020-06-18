InstaNotifier
=============

Checking for new feed entries periodically, accumulates new entries and sends the notifications.
UI is implemented in React.js. Allows rating, bookmarking, filtering, searching.
(UI demo is deployed to Heroku free dyno `instanotifier-react.herokuapp.com`_)

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django

=======

* Python: 3.7
* Django: 2.2
* React.js
* Celery
* ElasticSearch
* PostgreSQL
* License: MIT


Introductory Documentation
==========================

Goal
----
Periodically check for updates on some source (RSS, API, etc.), store new entries into db, and send notifications about the new ones (email, FB Messenger, push, Slack, etc.).

Components
----------
**Fetcher** → **Parser** → **Model**  → **Publisher**

**Fetcher**  ← *(source from where to fetch)* ← **FeedSource settings** → (*target where to send notification)* → **Publisher**


:Fetcher: Gets data from the particular source (RSS, API)
:Parser: Serialize the data fetched from the particular source into some model instance
:Filter: Having the set of new data entries, filters out the existing ones
:Model: Saves the data into the db
:Publisher: Sends out the data into the particular channel (email, fb messenger, etc.)
:FeedSource Settings: The settings application for wiring up the source to fetch from to the target to publish notifications to
:API: REST API providing access to stored data
:UI: Displays the stored entries, supports filtering and searching

Implemented functionality
-------------------------

* Modular architecture
* RssFetcher → RssParser → RssNotification model → Email publisher
* FeedSource settings application
* Using of FeedSource instance data in the RssFetcher and Email publisher
* Celery tasks with the hardcoded schedule to run the fetching.
* Integration with Mailgun (out of box from the cookiecutter project template)
* REST API for listing, rating, searching, filtering of stored entries
* UI for listing of saved RssNotifications. Allows rating of items, searching, filtering by date
* The demo of UI is deployed to Heroku `instanotifier-react.herokuapp.com`_ (It is a free dyno, so wait a little for it to wake up).  [NOTE: That deployed instance doesn't fetch any data from the sources, because the Celery is not deployed there. It only shows the already preloaded data.]

.. _`instanotifier-react.herokuapp.com`: https://instanotifier-react.herokuapp.com


Basic Commands
--------------

Building the front-end
^^^^^^^^^^^^^^^^^^^^^^

To build the dev environment:

.. code-block:: bash

    cd front-end
    npm start

To build the production environment:

.. code-block:: bash

    cd front-end
    npm run build


Celery
^^^^^^

To run celery:

.. code-block:: bash

    cd instanotifier
    celery -A instanotifier.taskapp worker -B -l info


Running tests
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ ./manage.py test


Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server `MailHog`_ with a web interface is available as docker container.

.. _mailhog: https://github.com/mailhog/MailHog

Container mailhog will start automatically when you will run all docker containers.
Please check `cookiecutter-django Docker documentation`_ for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html



Local Dev Setup
----------------

Starting up with `tmuxinator` locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the ``tmuxinator-inr.yml`` script provided, follow the TODOs in the script to set it up for your environment.
