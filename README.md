# Errbot Backend for Mattermost

**Thanks** to http://errbot.io and for the bot.
Most of this code was build with help from the already existing backends,
especially:
https://github.com/errbotio/errbot/blob/master/errbot/backends/slack.py

I can not guarantee that this is currently working 100%.
It probably has quite a few bugs as it is.

### KNOWN (POSSIBLE) ISSUES

- Channelmentions in messages aren't accounted for
- Nothing regarding files works
- Colors  in messages aren't working, mattermost does not have this afaik
- Probably a lot more

### INSTALLATION

Download this backend.
Install the backends requirements. 
Open errbot's config.py:

```
BACKEND = 'mattermost'
BOT_EXTRA_BACKEND_DIR = '/path/to/backends'

BOT_ADMINS = ('@yourname') # Names need the @ in front!
```

### INFO

This bot brings its own api and mattermost client implemantation,
since there wasn't anything complete enough/no python client at all.
This is probably going to change.
