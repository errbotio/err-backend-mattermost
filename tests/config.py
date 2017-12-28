##########################################################################
#                                                                        #
#  This is the config-template for Err. This file should be copied and   #
#  renamed to config.py, then modified as you see fit to run Errbot      #
#  the way you like it.                                                  #
#                                                                        #
#  As this is a regular Python file, note that you can do variable       #
#  assignments and the likes as usual. This can be useful for example if #
#  you use the same values in multiple places.                           #
#                                                                        #
#  Note: Various config options require a tuple to be specified, even    #
#  when you are configuring only a single value. An example of this is   #
#  the BOT_ADMINS option. Make sure you use a valid tuple here, even if  #
#  you are only configuring a single item, else you will get errors.     #
#  (So don't forget the trailing ',' in these cases)                     #
#                                                                        #
##########################################################################

import logging
import os

local_dir_path = os.path.dirname(__file__)

##########################################################################
# Core Errbot configuration                                              #
##########################################################################

BACKEND = 'Mattermost'
BOT_EXTRA_BACKEND_DIR = os.path.join(local_dir_path, '..')

BOT_ADMINS = ('@gpr')  # Names need the @ in front!
BOT_IDENTITY = {
    # Required
    'team': 'default',
    'server': '0.0.0.0',
    # For the login, either
    'login': 'errbot',
    'password': 'errbot',
    # Optional
    'insecure': True,  # Default = False. Set to true for self signed certificates
    'scheme': 'http',  # Default = https
    'port': 8080,  # Default = 8065
    'timeout': 30,  # Default = 30. If the webserver disconnects idle connections later/earlier change this value
    'cards_hook': 'osjx5d4ijfft58pf4tyci79jhh'  # Needed for cards/attachments
}

STORAGE = 'Memory'
BOT_DATA_DIR = os.path.join(local_dir_path, 'data')
BOT_EXTRA_PLUGIN_DIR = os.path.join(local_dir_path, 'plugins')
PLUGINS_CALLBACK_ORDER = (None, )
AUTOINSTALL_DEPS = True
BOT_LOG_FILE = BOT_DATA_DIR + '/err.log'
BOT_LOG_LEVEL = logging.DEBUG
BOT_LOG_SENTRY = False
SENTRY_DSN = ''
SENTRY_LOGLEVEL = BOT_LOG_LEVEL
BOT_ASYNC = False
BOT_ADMINS_NOTIFICATIONS = ('@gpr')
BOT_PREFIX = '!'

#BOT_PREFIX_OPTIONAL_ON_CHAT = False
#BOT_ALT_PREFIXES = ('Err',)
#BOT_ALT_PREFIX_SEPARATORS = (':', ',', ';')
#BOT_ALT_PREFIX_CASEINSENSITIVE = True
#HIDE_RESTRICTED_COMMANDS = False
#HIDE_RESTRICTED_ACCESS = False

# A list of commands which should be responded to in private, even if
# the command was given in a MUC. For example:
# DIVERT_TO_PRIVATE = ('help', 'about', 'status')
DIVERT_TO_PRIVATE = ('status', 'help', 'about')

# A list of commands which should be responded to in a thread if the backend supports it.
# For example:
# DIVERT_TO_THREAD = ('help', 'about', 'status')
DIVERT_TO_THREAD = ('divert_to_thread')

# Chat relay
# Can be used to relay one to one message from specific users to the bot
# to MUCs. This can be useful with XMPP notifiers like for example the
# standard Altassian Jira which don't have native support for MUC.
# For example: CHATROOM_RELAY = {'gbin@localhost' : (_TEST_ROOM,)}
CHATROOM_RELAY = {}

# Reverse chat relay
# This feature forwards whatever is said to a specific user.
# It can be useful if you client like gtalk doesn't support MUC correctly
# For example: REVERSE_CHATROOM_RELAY = {_TEST_ROOM : ('gbin@localhost',)}
REVERSE_CHATROOM_RELAY = {}

# Allow messages sent in a chatroom to be directed at requester.
#GROUPCHAT_NICK_PREFIXED = False

# Disable table borders, making output more compact (supported only on IRC, Slack and Telegram currently).
COMPACT_OUTPUT = True

# Disables the logging output in Text mode and only outputs Ansi.
# TEXT_DEMO_MODE = False

# Prevent ErrBot from saying anything if the command is unrecognized.
SUPPRESS_CMD_NOT_FOUND = False
