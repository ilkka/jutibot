"""A plugin for telling people when there is coffee."""

import logging
import re

from errbot import BotPlugin, botcmd, webhook
import explorerhat  # pylint: disable=import-error

LOG = logging.getLogger('errbot.plugin.FreshPots')


class FreshPots(BotPlugin):  # pylint: disable=too-many-ancestors
    """Fresh pots plugin class"""
    min_err_version = '3.2.0'  # Optional, but recommended
    max_err_version = '4.0.0'  # Optional, but recommended

    def __init__(self, bot):
        super(FreshPots, self).__init__(bot)
        self.bot_nick = bot.bot_config.CHATROOM_FN
        self.channels = []
        LOG.debug("Expecting nick to be %s", self.bot_nick)

    def activate(self):
        """Triggers on plugin activation

        You should delete it if you're not using it to override any default behaviour"""
        super(FreshPots, self).activate()

        if 'channels' in self:
            self.channels = self['channels']

        self.configure(self.get_configuration_template())
        LOG.info("konffis on %s", self.config)

        # start listening on a button
        explorerhat.touch.one.pressed(self.fresh_pots)

    def fresh_pots(self, _iochannel, _event):
        """Triggered by the hardware, send message."""
        LOG.info("Would send %s", self.config['image_url'])
        LOG.info("Channels is %s", self.channels)
        for dst in self.channels:
            self.send(dst, self.config['image_url'], message_type='groupchat')

    def deactivate(self):
        """Triggers on plugin deactivation

        You should delete it if you're not using it to override any default behaviour"""
        self['channels'] = self.channels
        super(FreshPots, self).deactivate()

    def get_configuration_template(self):
        """Defines the configuration structure this plugin supports

        You should delete it if your plugin doesn't use any configuration like this"""
        return {
            'image_url': 'https://i.imgur.com/510LaLV.gifv'
        }

    def check_configuration(self, configuration):
        """Triggers when the configuration is checked, shortly before activation

        You should delete it if you're not using it to override any default behaviour"""
        super(FreshPots, self).check_configuration(configuration)

    def callback_connect(self):
        """Triggers when bot is connected

        You should delete it if you're not using it to override any default behaviour"""
        pass

    def bot_msg_regex(self, message):
        """Construct a regex for matching a bot message.

        Args:
            message (str): regex fragment matching message body.

        Returns:
            regex that matches bot nick followed by message body.
        """
        return r'@?%s[:,]?\s*%s' % (self.bot_nick, message)

    def callback_message(self, message):
        """Triggered for every received message that isn't coming from the bot itself

        You should delete it if you're not using it to override any default behaviour"""
        # frm: sender userid
        # to: channel id
        # body: text incl nick
        if message.type == 'groupchat':
            if re.match(self.bot_msg_regex(r"(ilmoita|kerro|sano)\s+(täällä|tänne|tähän)"), message.body):
                self.channels.append(message.to)
                self['channels'] = self.channels
                self.send(message.to, "ok, alan ilmoittaa täällä",
                          in_reply_to=message, message_type='groupchat',
                          groupchat_nick_reply=True)

    @botcmd
    def debugsay(self, msg, args):
        self.fresh_pots(None, None)
