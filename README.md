# Errbot Backend for Mattermost

**Thanks** to http://errbot.io for the bot.
Most of this code was build with help from the already existing backends,
especially:
https://github.com/errbotio/errbot/blob/master/errbot/backends/slack.py
(If there is an Issue with any code I reused, please give me a message!)

It probably has quite a few bugs as it is.

## Experimental APIv4 Support
You can try out the apiv4 branch if you want some unstable experience! :-)

**Attention**: The `BOT_IDENTITY` config options have changed!

### KNOWN (POSSIBLE) ISSUES

- Channelmentions in messages aren't accounted for (Unsure if they need to be)
- ~~Nothing regarding files works~~ Info about files in a post are attached to the message

### REQUIREMENTS
- Python >= 3.4 (3.3 should work too)
- websockets 3.2
- [mattermostdriver](https://github.com/Vaelor/python-mattermost-driver) > 0.3.0

### INSTALLATION

- `git clone https://github.com/Vaelor/errbot-mattermost-backend.git`
- Create an account for the bot on the server.
- Install the requirements.
- Open errbot's config.py:

```
BACKEND = 'Mattermost'
BOT_EXTRA_BACKEND_DIR = '/path/to/backends'

BOT_ADMINS = ('@yourname') # Names need the @ in front!

BOT_IDENTITY = {
        # Required
        'login': 'bot@email.de',
        'password': 'botpassword',
        'team': 'nameoftheteam',
        'server': 'mattermost.server.com',
        # Optional
        'insecure': False, # Default = False. Set to true for self signed certificates
        'scheme': 'https', # Default = https
        'port': 8065, # Default = 8065
        'timeout': 30 # Default = 30. If the webserver disconnects idle connections later/earlier change this value
}
```

- If the bot has problems doing some actions, you should make it system admin, some actions won't work otherwise.


### FAQ

##### The Bot does not answer my direct messages
If you have multiple teams, check that you are both members of the same team!

