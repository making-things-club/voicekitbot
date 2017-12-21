#!env/bin/python

from slackclient import SlackClient
from importlib import import_module
from time import sleep
import config
import os


class Bot():
    def __init__(self):
        self.sc = SlackClient(config.slack["api_key"])
        self.users = self.sc.api_call("users.list")
        self.channel = config.slack["channel_name"]

        self.bot_user = self.get_user_id_by_name(
            config.slack["bot_name"])

        self.awkbot_user = self.get_user_id_by_name(
            config.slack["awkbot_name"])

    def post(self, message):
        self.sc.api_call(
            "chat.postMessage",
            channel=self.channel,
            text="<@%s> %s" % (self.awkbot_user, message),
            as_user=self.bot_user
        )

    def log(self, message):
        self.sc.api_call(
            "chat.postMessage",
            channel=self.channel,
            text="_%s_" % message,
            as_user=self.bot_user
        )

    def get_user_id_by_name(self, user_name):
        for user in self.users["members"]:
            if user["name"] == user_name:
                return user["id"]
