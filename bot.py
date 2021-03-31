from configparser import ConfigParser
import logging
from typing import Optional, Union
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, Handler

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

config = ConfigParser()
config.read("bot.ini")

TOKEN = config.get("DEFAULT", "token")

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


class CustomHandler(Handler):
    def check_update(self, update: object) -> Optional[Union[bool, object]]:
        return super().check_update(update)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def write(update, context):
    context.bot.send_message(chat_id="@grupoprueva", text="this is a test")


def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(), title="Caps", input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


def main():
    start_handler = CommandHandler("start", start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    inline_caps_handler = InlineQueryHandler(inline_caps)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(CustomHandler())
    dispatcher.add_handler(CommandHandler("write", write))
    dispatcher.add_handler(inline_caps_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

"""
2021-03-28 04:05:56,477 - telegram.ext.dispatcher - DEBUG - Processing Update: {'update_id': 635103143, 'message': {'message_id': 3, 'date': 1616918769, 'chat'
: {'id': -1001259463233, 'type': 'supergroup', 'title': 'Grupo prueba', 'username': 'grupoprueva'}, 'entities': [], 'caption_entities': [], 'photo': [], 'new_c
hat_members': [], 'left_chat_member': {'id': 1703229037, 'first_name': 'RaulyEnterprise', 'is_bot': True, 'username': 'rauly_bot'}, 'new_chat_photo': [], 'dele
te_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 'from': {'id': 622490424, 'first_name': 'l
uisiacc', 'is_bot': False, 'username': 'Luisiacc', 'language_code': 'es'}}}

2021-03-28 04:09:16,342 - telegram.ext.dispatcher - DEBUG - Processing Update: {'update_id': 635103144, 'my_chat_member': {'chat': {'id': -1001259463233, 'type
': 'supergroup', 'title': 'Grupo prueba', 'username': 'grupoprueva'}, 'date': 1616918969, 'old_chat_member': {'user': {'id': 1703229037, 'first_name': 'RaulyEn
terprise', 'is_bot': True, 'username': 'rauly_bot'}, 'status': 'left', 'until_date': None}, 'new_chat_member': {'user': {'id': 1703229037, 'first_name': 'Rauly
Enterprise', 'is_bot': True, 'username': 'rauly_bot'}, 'status': 'member', 'until_date': None}, 'from': {'id': 622490424, 'first_name': 'luisiacc', 'is_bot': F
alse, 'username': 'Luisiacc', 'language_code': 'es'}}}
2021-03-28 04:09:16,606 - telegram.bot - DEBUG - Getting updates: [635103145]
2021-03-28 04:09:16,606 - telegram.bot - DEBUG - [<telegram.update.Update object at 0x7f455b7addc0>]
2021-03-28 04:09:16,606 - telegram.bot - DEBUG - Exiting: get_updates
2021-03-28 04:09:16,606 - telegram.bot - DEBUG - Entering: get_updates
2021-03-28 04:09:16,607 - telegram.ext.dispatcher - DEBUG - Processing Update: {'update_id': 635103145, 'message': {'message_id': 4, 'date': 1616918969, 'chat'
: {'id': -1001259463233, 'type': 'supergroup', 'title': 'Grupo prueba', 'username': 'grupoprueva'}, 'entities': [], 'caption_entities': [], 'photo': [], 'new_c
hat_members': [{'id': 1703229037, 'first_name': 'RaulyEnterprise', 'is_bot': True, 'username': 'rauly_bot'}], 'new_chat_photo': [], 'delete_chat_photo': False,
 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 'from': {'id': 622490424, 'first_name': 'luisiacc', 'is_bot': Fa
lse, 'username': 'Luisiacc', 'language_code': 'es'}}}
    """
