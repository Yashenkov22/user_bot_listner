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
    'валюта': r"\bвалют\w*\b",
    # 'денег': r"\bденег\b",
    'деньги': r"\bденьги\w*\b",
    'наличные': r"\bналичные\w*\b",
    # 'usdt': r"\busdt\w*\b",
    # 'юсдт': r"\bюсдт\w*\b",
    # 'trc20': r"\btrc20\w*\b",
    # '$': r"\$",
    # 'доллары': r"\bдоллары\w*\b",
    # 'баксы': r"\bбаксы\w*\b",
    # 'руб': r"\bруб\w*\b",
    # 'rub': r"\brub\w*\b",
    # 'лиры': r"\bлиры\w*\b",
}

# BLACK_LIST_PATTERNS = (
#     r"\bпиши в личку\w*\b",
#     r"\bпиши в лc\w*\b",
#     r"\bпишите в личные сообщения\w*\b",
#     r"\bвыкупаем\w*\b",
#     r"\bбуду благодарен за репост\w*\b",
#     r"\bжду вас в – лс\w*\b",
#     r"\bпиши мне \"+\"\w*\b",
#     r"\bкупим ваш\w*\b",
#     r"\bкурс вам понравится\w*\b",
#     r"\bлучший курс\w*\b",

# )


BLACK_LIST_PATTERNS = (
    r"пиши в личку",
    r"пиши в лс",
    r"пишите в личные сообщения",
    r"выкупаем",
    r"буду благодарен за репост",
    r"жду вас в\s*–?\s*лс",
    r'пиши мне\s*"\+"',
    r"купим ваш",
    r"курс вам понравится",
    r"пишите в лс",
    r"пишите в личку",
    r"скупаю юсдт",
    r"скамерам не писать",
    r"ищу обмен",
    r"личная встреча",
    r"офис или встреча",
    r"tether",
    r"личка открыта",
    r"в лс",
    r"поможем с",
    r"пиcать в лс",
    r"доставка по городу",
    r"exchange",
    r"кэш",
    r"трахаюсь",
    r"секс",
    r"при личной встрече",
    r"прибыль",
    r"по хорошей цене",
    r"выкупаю",
    r"сможет продать",

    r"обмен крuпты лично",
    r"выгoдно и безопасно",
    r"пиcать в лс",
    r"приобретаю usdt",
    r"консультация",
    r"срочно покупаем usdt",
    r"интересует usdt",
    r"всё при встрече",
    r"предлагаю хороший курс",
    r"работаю по всему миру",
    r"только встреча",
    r"в курсе",
    r"хорошей репутацией",
    r"куплю usdt за наличные",
    r"покупка usdt за наличные",
    r"реальная встреча",
    r"бесплатное обучение",
    r"идет набор команды",
    r"криптожара",
    r"индивидуальный подход",

    r"покупаю usdt с реальными курсами",
    r"без скрытых комиссий",
    r"без обмана и предоплат",
    r"пишите, обсудим",
    r"whatsapp",
    r"куплю юсдт за наличные",
    r"хочешь обменять usdt",
    r"связь в л\.с\.",

    r"самые низкие цены на рынке",
    r"стол в стол",
    r"курс договоримся",
    r"рассматриваю покупку usdt",
    r"скупаем usdt",
    r"без предоплат и комиссий",
    r"могу выдать наличные",

    r"сделаем все быстро",
    r"перевод без комиссии",
    r"обменяю юсдт на наличку",
    r"доставка бесплатно",
    r"курс зависит от обьема",
    r"никаких переплат",
    r"круглосуточно и без выходных",

    r"для обмена пишите оператору",
    r"покупаю юсдт по адекватному курсу",
    r"готов на обмен",
    r"работаю 24/7",
    r"работаем быстро",
    r"купить юсдт по хорошему курсу",

    r"курсы английского языка",
    r"моментально",
    r"работаем в любом городе",
    r"плачу налом за тезер",
    r"f-1",
    r"языковые курсы",
    r"зaрaбoтoк удaленнo",
    r"покупаю usdt и usdc",

    r"пиши — всё обсудим",
    r"продажа — по лучшему курсу",
    r"Принимаем usdt",
    r"стол на стол",
    r"нужен обмен",
    r"работаем в любом городе",
    r"сапборд",
    r"сап борд",
    r"плачу налом за тезер",
    r"встречусь лично",
    r"курс приятный",

    r"скупаю",
    r"нужен обмен",
    r"нужен юсдт",
    r"конвертор",
    r"золотая корона",
    r"гарантируем анонимность",
    r"аренда",
    r"сотрудничеств\w*\b",
    r"старого образца",

    r"старый образец",
    r"лучшие цены",
    r"работаю честно",
)


@client.on(events.NewMessage)
async def listen_any_message(event):
    asyncio.create_task(process_event(event))


async def process_event(event):
    text = event.raw_text.lower()
    # async for dialog in client.iter_dialogs():
    #     print(f"Название: {dialog.name} | ID: {dialog.id} | Тип: {type(dialog.entity)}")
    # msg = event.message

    if not event.sender or event.sender.bot:
        return

    chat_to = '@test_userbot22'

    for pattern_word, pattern in PATTERNS.items():
        try:
            # print(f'проверяю {pattern_word}...')
            if re.search(pattern, text):
                # black list words
                if any(re.search(black_pattern, text) for black_pattern in BLACK_LIST_PATTERNS):
                    print('black pattern!')
                    return
                # print('успешно')

                user_data = event.sender

            # print('user', user_data)
                chat: types.Channel = event.chat

                print('chat', chat.__dict__)

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
