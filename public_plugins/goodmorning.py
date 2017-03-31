import asyncio
import string

print("[Public Plugin] <goodmorning.py>: This plugin says good morning.")

good_morning_count = 0
inbetween_messages = 0
users_morning = []


@asyncio.coroutine
def action(message, client, config):
    global good_morning_count
    global users_morning
    global inbetween_messages
    print(good_morning_count)

    good_morning_strings = ["good morning", "gmorning", "morning"]

    exclude = set(string.punctuation)
    cleaned_str = ''.join(ch for ch in message.content if ch not in exclude).lower()
    clean_user = str(message.author).split("#")[0]

    if cleaned_str in good_morning_strings and clean_user not in users_morning:
        good_morning_count += 1
        users_morning.append(clean_user)

        if good_morning_count >= 2:
            users_morning = []
            good_morning_count = 0
            yield from client.send_message(message.channel, "Good morning!")
    else:
        inbetween_messages += 1

        if inbetween_messages >= 3:
            inbetween_messages = 0
            print("resetting good morning count")
            users_morning = []
            good_morning_count = 0

