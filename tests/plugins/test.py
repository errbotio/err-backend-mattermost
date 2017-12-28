# -*- coding: utf-8 -*-

from errbot import BotPlugin, botcmd, webhook
import re


class TestPlugin(BotPlugin):
    """
    Fill in your plugin description here.
    """

    def activate(self):
        """
        Triggers on plugin activation

        You should delete it if you're not using it to override any default behaviour
        """
        super(TestPlugin, self).activate()

    def deactivate(self):
        """
        Triggers on plugin deactivation

        You should delete it if you're not using it to override any default behaviour
        """
        super(TestPlugin, self).deactivate()

    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports

        You should delete it if your plugin doesn't use any configuration like this
        """
        return {'EXAMPLE_KEY_1': "Example value",
                'EXAMPLE_KEY_2': ["Example", "Value"]
                }

    def check_configuration(self, configuration):
        """
        Triggers when the configuration is checked, shortly before activation

        You should delete it if you're not using it to override any default behaviour
        """
        super(TestPlugin, self).check_configuration()

    def callback_connect(self):
        """
        Triggers when bot is connected

        You should delete it if you're not using it to override any default behaviour
        """

        pass

    def callback_message(self, message):
        """
        Triggered for every received message that isn't coming from the bot itself

        You should delete it if you're not using it to override any default behaviour
        """
        if re.compile("^!.*$").match(message.body):
            pass

        # Threaded message
        self.send(in_reply_to=message, identifier=message.to,
                  text="Call back threaded message")

        # Single message
        self.send(identifier=message.to, text="Call back single message")

        #
        self.send(identifier=message.frm, text="Call back 1to1  message")

        pass

    def callback_botmessage(self, message):
        """
        Triggered for every message that comes from the bot itself

        You should delete it if you're not using it to override any default behaviour
        """
        pass

    @webhook
    def example_webhook(self, incoming_request):
        """A webhook which simply returns 'Example'"""
        return "Example"

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @botcmd(split_args_with=None)
    def example(self, mess, args):
        """A command which simply returns 'Example'"""
        return "This message SHOULD NOT have created a thread"

    # Passing split_args_with=None will cause arguments to be split on any kind
    # of whitespace, just like Python's split() does
    @botcmd(split_args_with=None)
    def divert_to_thread(self, mess, args):
        """A command which simply returns 'Example'"""
        return "This message SHOULD have created a thread"
