.. _user_guide:

User Guide
========================================================================

.. contents:: :local:

Cards/Attachments
------------------------------------------------------------------------

Cards are called _attachments_ in Mattermost.

If you want to send attachments, you need to create an incoming Webhook in Mattermost
and add the webhook id to your errbot `config.py` in `BOT_IDENTITY`.

This is not an ideal solution, but AFAIK Mattermost does not support sending attachments
over the api like slack does.


APIv3
------------------------------------------------------------------------
Mattermost has deprecated the v3 API.  If you are still running APIv3, you're strongly encourage to upgrade.
Despite this, there is an APIv3 branch in the github repository that you can try but keep in mind that it is no longer supported and not guaranteed to work!  

.. important:: The `BOT_IDENTITY` config options are different for APIv3 and APIv4!


Known (possible) Issues
------------------------------------------------------------------------

- Channel mentions in messages aren't accounted for and it is unclear if they need to be.  If you think they should be or you've encountered an error, please open an issue against the err-backend-mattermost github repository.


F.A.Q.
------------------------------------------------------------------------

The Bot does not answer my direct messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you have multiple teams, check that you are both members of the same team!


Special thanks
------------------------------------------------------------------------

**Thanks** to http://errbot.io/ the contributors.  The mattermost backend has been derived from the backends from there.
