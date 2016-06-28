#!/usr/bin/python3

import datetime
import random
import re

import telegram.botapi.botbuilder as botbuilder

IGNORED_CHARACTERS = "ß"

PREFIXES = ["surely you meant",
            "say it loud, say it proud",
            "u wot m8",
            "heresy against the caps",
            "scream it like you mean it",
            "shame",
            "traitor",
            "it's capslock tuesday you wanker",
            "look here, this is how it works",
            "i'm gonna help you a little bit since it seems you can't figure it out",
            "oh golly, another one"]

URL_PATTERN = r"(http[s]?://)?([a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+){1}(\.[a-zA-Z0-9\-_]+)*(/[a-zA-Z0-9\-_\.]*)*(\.?[a-zA-Z0-9\-_\?=&]+){1}(#[a-zA-Z0-9\.\-_\?=&]+)?"
URL_REGEX = re.compile(URL_PATTERN)

DISABLED_CHATS = []

def remove_urls(text):
    while True:
        m = False
        for match in URL_REGEX.finditer(text):
            m = True
            print("found url", match.group())
            text = text[:match.start()] + text[match.end():]
            print("new text is", text)
        if not m:
            break
    return text

def was_sent_on_tuesday(date):
    d = datetime.datetime.fromtimestamp(int(date))
    return d.isoweekday() == 2

def text_is_lowercase(update):
    print(update)
    if update.chat.id in DISABLED_CHATS:
        return False
    if not update.text:
        return False
    if was_sent_on_tuesday(update.date):
        text = remove_urls(update.text)
        for c in text:
            if c in IGNORED_CHARACTERS:
                pass
            elif c.islower():
                return True
    return False

def shame(update):
    text = "*" + PREFIXES[random.randint(0, len(PREFIXES)-1)].upper() + ":* \""
    for c in update.text:
        if c in IGNORED_CHARACTERS:
            text = text + c
        else:
            text = text + c.upper()
    text = text + "\" !!!"
    return text

def enable(update):
    print("enabling bot for chat", update.chat.id)
    DISABLED_CHATS.remove(update.chat.id)

def disable(update):
    print("disabling bot for chat", update.chat.id)
    if not update.chat.id in DISABLED_CHATS:
        DISABLED_CHATS.append(update.chat.id)

if __name__ == "__main__":
    while True:
        try:
            bot = botbuilder.BotBuilder(apikey_file="key.txt") \
                .do_when("enable", enable, True)\
                .do_when("disable", disable, True)\
                .send_message_when(text_is_lowercase, shame, optionals={"parse_mode":"Markdown"}) \
                .build()
            bot.start()
        except Exception as e:
            print(e)
