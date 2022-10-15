.. _installation:

Installation
========================================================================

.. contents:: :local:

Requirements
------------------------------------------------------------------------

 - Mattermost with APIv4
 - Python >= 3.7
 - websockets 3.2
 - `mattermostdriver <https://github.com/Vaelor/python-mattermost-driver>`_ > 4.0


Python Virtual Environment
------------------------------------------------------------------------

These instructions assume you have a mattermost instance up and running with a bot account configured.  For information on how to setup the bot account see https://developers.mattermost.com/integrate/reference/bot-accounts/

    1. Create a virtual environment for errbot.
    ::

        python3 -m venv <path_to_virtualenv>
        source <path_to_virtualenv>/bin/activate

    2. Install errbot and mattermost backend.
    ::

        pip install errbot mattermost

    3. Initialise errbot and configure mattermost.
    ::

        errbot --init

    4. See the :ref:`configuration` section for configuration details.
