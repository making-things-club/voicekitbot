#!/usr/bin/env python3

import logging
import subprocess
import sys
import os

import aiy.assistant.auth_helpers
import aiy.audio
import aiy.voicehat

import config

from importlib import import_module

from google.assistant.library import Assistant
from google.assistant.library.event import EventType

from slackbot import Bot

# logging.basicConfig(
#    level=logging.INFO,
#    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
# )


class Voicekitbot():
    def __init__(self):
        self.bot = Bot()
        self.gather_commands()

        credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
        with Assistant(credentials) as assistant:
            for event in assistant.start():
                self.process_event(assistant, event)

    def gather_commands(self):
        self.modules = {}
        self.actions = {}

        for root, dirs, files in os.walk("voicekitbot/commands"):
            for file in files:

                if (not file.endswith(".py")) or file.startswith("__"):
                    continue

                path_name = root.replace("voicekitbot/", "")
                path_name = path_name.replace("/", ".")
                module_name = file.replace(".py", "")

                module = import_module("%s.%s" % (path_name, module_name))

                init = getattr(module, "init")
                init(config)

                list_actions = getattr(module, "list_actions")

                self.modules[module_name] = module
                self.actions[module_name] = list_actions()

    def process_event(self, assistant, event):
        if event.type == EventType.ON_START_FINISHED:
            self.log('ready')
            if sys.stdout.isatty():
                self.log('Say "OK, Google" then speak, or press Ctrl+C to quit...')

        elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
            self.log('listening')

        elif event.type == EventType.ON_END_OF_UTTERANCE:
            self.log('thinking')

        elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
            self.log('ready')

        elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
            self.log('something killed me...')
            sys.exit(1)

        elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
            self.process_command(assistant, event.args['text'])

    def process_command(self, assistant, text):
        text = text.lower()
        self.log("I think you just said '%s'" % text)
        for module_name, module in self.modules.items():
            for action in self.actions[module_name]:
                for message in action["content"]:
                    if text == message:
                        assistant.stop_conversation()

                        func = getattr(module, action["function"])
                        command = func(text)

                        aiy.audio.say(command["say"])
                        self.bot.post(command["post"])

        if (text == "what can we do"):
            assistant.stop_conversation()
            self.list_commands()

    def list_commands(self):
        msg = "```Available commands:\r"
        for module_name, module in self.modules.items():
            msg += "\r%s:\r" % module_name
            for action in self.actions[module_name]:
                msg += "- *%s*: %s\r" % (
                    '/'.join(action["content"]), action["description"])
        msg += "```"
        self.log(msg)

    def log(self, message):
        status_ui = aiy.voicehat.get_status_ui()
        status_ui.status(message)
        self.bot.log(message)


voicekitboy = Voicekitbot()
