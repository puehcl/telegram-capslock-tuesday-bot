import datetime

import telegram.botapi.botbuilder as botbuilder


def was_sent_on_tuesday(date):
    d = datetime.datetime.fromtimestamp(int(date))
    return d.isoweekday() == 2

def text_is_lowercase(update):
    print(update)
    if not update.text:
        return False
    if was_sent_on_tuesday(update.date):
        for c in update.text:
            if c.islower():
                return True
    return False

def shame(update):
    result = "*SHAME:* "
    shaming = False
    for c in update.text:
        if c.islower():
            if not shaming:
                result = result + " *"
            result = result + c
            shaming = True
        elif c.isalpha():
            if shaming:
                result = result + "* "
            result = result + c
            shaming = False
        else:
            result = result + c
    if shaming:
        result = result + "* "
    return result

if __name__ == "__main__":
    bot = botbuilder.BotBuilder(apikey_file="key.txt") \
        .send_message_when(text_is_lowercase, shame, optionals={"parse_mode":"Markdown"}) \
        .build()
    bot.start()
