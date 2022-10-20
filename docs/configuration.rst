.. _configuration:

Configuration
========================================================================

To configure mattermost as errbot's backend, you must edit `config.py`, which is created as part of the errbot initialisation process or downloaded from the official errbot documentation.


.. code-block:: python

    BACKEND = 'Mattermost'
    BOT_EXTRA_BACKEND_DIR = '/path/to/backends'

    BOT_ADMINS = ('@yourname') # Names need the @ in front!

    BOT_IDENTITY = {
        # Required
        "team": "nameoftheteam",
        "server": "mattermost.server.com",
        # For the login, either
        "login": "bot@email.de",
        "password": "botpassword",
        # Or, if you have a personal access token
        "token": "YourPersonalAccessToken",
        # Optional
        "insecure": False,                  # Default = False. Set to true for self signed certificates
        "scheme": "https",                  # Default = https
        "port": 8065,                       # Default = 8065
        "timeout": 30,                      # Default = 30. If the web server disconnects idle connections later/earlier change this value
        "cards_hook": "incomingWebhookId"   # Needed for cards/attachments
    }


.. note:: The above configuration example only shows mattermost settings, but all errbot configuration settings.  Use the official errbot documentation to complete the above example.

.. important:: Some Mattermost actions can only be performed with administrator rights.  If the bot has problems performing an action, check the bot account permissions and grant the appropriate rights.
