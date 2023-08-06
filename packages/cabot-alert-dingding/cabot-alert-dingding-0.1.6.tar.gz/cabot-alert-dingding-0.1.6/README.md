==========================
Cabot Dingding Alert Plugin
==========================

A plugin for `Cabot`_ service monitoring that will post alerts to a URL.

The plugin will POST a payload like the following to a user-defined endpoint::

        payload = {
            "msgtype": "text", 
            "text": {
                "content": message
            }, 
            "at": {
                "atMobiles": [
                  service.name
                ], 
                "isAtAll": True
            }
        }

Installation
============

Install from pip::

    $ pip install cabot-alert-dingding

Edit `conf/*.env`::

    # add cabot_alert_dingding to your comma separated list
    CABOT_PLUGINS_ENABLED=cabot_alert_dingding

Run migrations and restart cabot::

    $ cabot migrate

.. _Cabot: https://cabotapp.com
