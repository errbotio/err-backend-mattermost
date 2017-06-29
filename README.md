# Errbot Backend for Mattermost

## APIv4 Support
The master branch is now set to use the new APIv4 for mattermost.
Some things have changed, please see the updated requirements and
changed BOT_IDENTITY parameters.

 - 'email' is now 'login'
 - 'server' is the url without https:// or the port. Port and scheme have their own option now.
 - You need to `pip install mattermostdriver`

### APIv3
Use the APIv3 branch for that.

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

# SPECIAL THANKS

**Thanks** to http://errbot.io and all the contributors to the bot.
Most of this code was build with help from the already existing backends,
especially:
https://github.com/errbotio/errbot/blob/master/errbot/backends/slack.py
(If there is an Issue with any code I reused, please give me a message!)
