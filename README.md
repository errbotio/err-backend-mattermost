# Errbot Backend for Mattermost

**Thanks** to http://errbot.io for the bot.
Most of this code was build with help from the already existing backends,
especially:
https://github.com/errbotio/errbot/blob/master/errbot/backends/slack.py
(If there is an Issue with any code I reused, please give me a message!)

It probably has quite a few bugs as it is.

### KNOWN (POSSIBLE) ISSUES

- Channelmentions in messages aren't accounted for (Unsure if they need to be)
- Nothing regarding files works

### REQUIREMENTS
- Python >= 3.4
- websockets 3.2

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
        'email': 'bot@email.de',
        'password': 'botpassword',
        'insecure': False, # Optional, default value is False. Set to true for self signed certificates
        'server': 'https://mattermost.kapsi.me',
        'team': 'nameoftheteam',
        'timeout': 30 # Optional, default value is 30. If the webserver disconnects idle connections later/earlier change this value
}
```

- If the bot has problems doing some actions, you should make it system admin, some actions won't work otherwise.

### INFO

This bot brings its own api and mattermost client implementation
since there wasn't anything complete enough/no python client for mattermost at all - none that I found at least.
I will probably do some changes there, maybe move the client into it's own repository.
