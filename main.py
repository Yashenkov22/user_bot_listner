import re
import asyncio
import pytz

from datetime import timedelta, datetime

from telethon import TelegramClient, events
from telethon import types

api_id = 25430288
api_hash = "08616908140d6688f2e0107805741d9d"
# session_name = "my_userbot"

loop = asyncio.get_event_loop()

client = TelegramClient('./telethon_userbot.session',
                        api_id=api_id,
                        api_hash=api_hash,
                        loop=loop)

moscow_tizone = pytz.timezone('Europe/Moscow')


# PATTERNS = [
#     r"\bобмен\w*\b",
#     r"\bкурс\w*\b",
#     r"\bвалют\w*\b",
#     r"\bденег\b",
#     r"\bденьг\w*\b",
#     r"\bналич\w*\b",
#     # r"\bскрининг\w*\b",
# ]

PATTERNS = {
    'обмен': r"\bобмен\w*\b",
    'курс': r"\bкурс\w*\b",
    'валют': r"\bвалют\w*\b",
    'денег': r"\bденег\b",
    'деньг': r"\bденьг\w*\b",
    'налич': r"\bналич\w*\b",
    'usdt': r"\busdt\w*\b",
    'юсдт': r"\bюсдт\w*\b",
    'trc20': r"\btrc20\w*\b",
    # '$': r"\$",
    'доллары': r"\bдоллары\w*\b",
    'баксы': r"\bбаксы\w*\b",
    'руб': r"\bруб\w*\b",
    'rub': r"\brub\w*\b",
    'лиры': r"\bлиры\w*\b",
}


@client.on(events.NewMessage)
async def listen_any_message(event):
    asyncio.create_task(process_event(event))


async def process_event(event):
    text = event.raw_text.lower()
    # msg = event.message

    if event.sender.bot:
        return

    chat_to = '@test_userbot22'

    for pattern_word, pattern in PATTERNS.items():
        try:
            # print(f'проверяю {pattern_word}...')
            if re.search(pattern, text):
                # print('успешно')

                user_data = event.sender

            # print('user', user_data)
                chat: types.Channel = event.chat

                chat_username = chat.username
                chat_name = chat.title

                try:
                    reply_to = event.message.reply_to
                    # print('REPLY TO ', reply_to)
                    topic_id = reply_to.reply_to_top_id

                    if topic_id is None:
                        raise Exception()
                    
                except Exception as ex:
                    print(ex)
                    try:
                        topic_id = reply_to.reply_to_msg_id
                    except Exception as ex:
                        print(ex)
                        topic_id = None

            # print('topic_id',topic_id)

                message_date = event.date + timedelta(hours=3)

                name = None

                if user_data:
                    username = user_data.username
                    first_name = user_data.first_name
                    last_name = user_data.last_name

                    name = username or first_name or last_name or f'Имя неизвестно, id {user_data.id}'

                if name is None:
                    name = f'Имя неизвестно'

                print(f'***\nСообщение из {chat_name}\n\nВремя: {datetime.now(tz=moscow_tizone)}\n***\n')

                user_id_link = f'tg://user?id={user_data.id}'

                _text = f'🔔 Сообщение из чата <a href="https://t.me/{chat_username}">{chat_name}</a>\n\nНайдено совпадение по ключевому слову: {pattern_word}\n\nТекст сообщения:\n<pre>\n{event.raw_text}</pre>\n\nПользователь: {name}\nВремя сообщения: {message_date.strftime("%d.%m.%Y %H:%M")}\n\nСсылки на пользователя:\n- по id: {user_id_link}'
                
                if user_data.username:
                    username_link = f'https://t.me/{user_data.username}'
                    _text += f'\n- по username: {username_link}'

                if topic_id:
                    url = f"https://t.me/{chat_username}/{topic_id}/{event.message.id}"
                else:
                    url = f"https://t.me/{chat_username}/{event.message.id}"

                _text += f'\n\n<a href="{url}"><b>Перейти к сообщению</b></a>'

                await client.send_message(chat_to,
                                        _text,
                                        parse_mode='HTML',
                                        link_preview=False)
                break
        except Exception as ex:
            print(ex)
            continue


client.start()

print('--- START USER BOT...')

client.run_until_disconnected()
