import sys
import ping3
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import logging
import settings

ping3.EXCEPTIONS = True
TOKEN = settings.API
# получаем экземпляр `Updater`
updater = Updater(token=TOKEN, use_context=True)
# получаем экземпляр `Dispatcher`
dispatcher = updater.dispatcher

logging.basicConfig(format='%(levelname)s - %(message)s - %(asctime)s - %(name)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

BIO, BIO2, BIO3 = range(3)


# функция обратного вызова точки входа в разговор
def start(update, _):
    # Список кнопок для ответа
    reply_keyboard = [['проверить']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Меня зовут профессор Бот. Я проведу с вами беседу. '
        'Команда /cancel, чтобы прекратить разговор.\n\n'
        'Проверим?',
        reply_markup=markup_key)
    # переходим к этапу `CHECK`, это значит, что ответ
    # отправленного сообщения в виде кнопок будет список
    # обработчиков, определенных в виде значения ключа `GENDER`
    return BIO


# Обрабатываем пол пользователя
# def gender(update, _):
#     # определяем пользователя
#     user = update.message.from_user
#     # Пишем в журнал пол пользователя
#     logger.info("Пол %s: %s", user.first_name, update.message.text)
#     # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
#     update.message.reply_text(
#         'Хорошо. Пришли мне свою фотографию, чтоб я знал как ты '
#         'выглядишь, или отправь /skip, если стесняешься.',
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     # переходим к этапу `PHOTO`
#     return PHOTO

def first_state(update, _):
    text = update.message.text
    _.bot.send_message(chat_id=update.effective_chat.id,
                       text=text)
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал биографию или рассказ пользователя
    logger.info("Пользователь %s рассказал: %s", user.first_name, update.message.text)
    # Отвечаем на то что пользователь рассказал.
    update.message.reply_text('Спасибо! \nВведи ip адрес для проверки ответа из внешней сети')
    return BIO2


def second_state(update, _):
    text = update.message.text
    update.message.reply_text(text)
    check(update, text)


def bio3(update, _):
    text = update.message.text
    _.bot.send_message(chat_id=update.effective_chat.id,
                       text=text)
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал биографию или рассказ пользователя
    logger.info("Пользователь %s рассказал: %s", user.first_name, update.message.text)
    # Отвечаем на то что пользователь рассказал.
    update.message.reply_text('Спасибо! Надеюсь, когда-нибудь снова сможем поговорить.')
    # Заканчиваем разговор.

    return ConversationHandler.END


# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет скучно - пиши.',
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END


# функция обратного вызова
def echo(update, context):
    # добавим в начало полученного сообщения строку 'ECHO: '
    text = 'ECHO: ' + update.message.text
    # `update.effective_chat.id` - определяем `id` чата,
    # откуда прилетело сообщение
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


# FOR TESTING NEEDS ========================================================
def check(update, ip):
    user = update.message.from_user

    def concat():
        l = log.messages
        return "".join([str(x) for x in l])

    try:
        log.start()
        ping3.verbose_ping(ip, count=6, size=1400)
        log.stop()
        print(log.messages)
        # context.bot.send_message(chat_id=update.effective_chat.id, text=concat())
        update.message.reply_text(concat() + "\nВсе хорошо. Хост доступен и отвечает.")

    except ping3.errors.TimeToLiveExpired as err:
        update.message.reply_text(concat() + err.ip_header["src_addr"])
    except ping3.errors.HostUnknown:
        print(log.messages)
        update.message.reply_text(concat() + "Неизвестный или неверный хост.")
    except ping3.errors.Timeout:
        print(log.messages)
        update.message.reply_text("Время запроса истекло, хост недоступен или не отвечает."
                                      "\n(Request timeout for ICMP packet)")
    except IndexError:
        print(log.messages)
        update.message.reply_text("Нет данных для проверки")
    except AttributeError:
        print(log.messages)
        update.message.reply_text("Хост не указан")
    except OSError:
        update.message.reply_text("Неверные данные")

    logger.info("Пользователь %s рассказал: %s", user.first_name, update.message.text)
    # Отвечаем на то что пользователь рассказал.
    update.message.reply_text('Спасибо! Надеюсь')
    return BIO3


# ===========================================================================

def caps(update, context):
    # если аргументы присутствуют
    if context.args:
        # объединяем список в строку и
        # переводим ее в верхний регистр
        text_caps = ' '.join(context.args).upper()
        # `update.effective_chat.id` - определяем `id` чата,
        # откуда прилетело сообщение
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text_caps)
    else:
        # если в команде не указан аргумент
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='No command argument')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='send: /caps argument')


#
# # Обратите внимание, что из обработчика в функцию
# # передаются экземпляры `update` и `context`
# def start(update, context):
#     user = update.message.from_user
#     name = user.first_name
#     # `bot.send_message` это метод Telegram API
#     # `update.effective_chat.id` - определяем `id` чата,
#     # откуда прилетело сообщение
#     context.bot.send_message(chat_id=update.effective_chat.id,
#                              text="O, "+name+", привет :)\nКак дела?")


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Неизвестная команда.")


class Logger:
    stdout = sys.stdout
    messages = []

    def start(self):
        self.messages.clear()
        sys.stdout = self

    def stop(self):
        sys.stdout = self.stdout

    def write(self, text):
        self.messages.append(text)


# logger Class to catch output from ping3 module to trace it to the TG chat
log = Logger()

conv_handler = ConversationHandler(  # здесь строится логика разговора
    # точка входа в разговор
    entry_points=[CommandHandler('start', start)],
    # этапы разговора, каждый со своим списком обработчиков сообщений
    states={
        BIO: [MessageHandler(Filters.text & ~Filters.command, first_state)],
        BIO2: [MessageHandler(Filters.text & ~Filters.command, second_state)],
        # LOCATION: [
        #     MessageHandler(Filters.location, location),
        #     CommandHandler('skip', skip_location),
        # ],
        BIO3: [MessageHandler(Filters.text & ~Filters.command, bio3)],
    },
    # точка выхода из разговора
    fallbacks=[CommandHandler('cancel', cancel)],
)

# Добавляем обработчик разговоров `conv_handler`
dispatcher.add_handler(conv_handler)

# говорим обработчику, если увидишь команду `/start`,
# то вызови функцию `start()`
start_handler = CommandHandler('start', start)
# добавляем этот обработчик в `dispatcher`
dispatcher.add_handler(start_handler)

# говорим обработчику `MessageHandler`, если увидишь текстовое
# сообщение (фильтр `Filters.text`)  и это будет не команда
# (фильтр ~Filters.command), то вызови функцию `echo()`
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
# регистрируем обработчик `echo_handler` в экземпляре `dispatcher`
dispatcher.add_handler(echo_handler)

# обработчик команды '/caps'
caps_handler = CommandHandler('caps', caps)
# регистрируем обработчик в диспетчере
dispatcher.add_handler(caps_handler)

# обработчик команды /ip
check_handler = CommandHandler('check', check)
# регистрируем обработчик в диспетчере
dispatcher.add_handler(check_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# запуск прослушивания сообщений
updater.start_polling()
# обработчик нажатия Ctrl+C
updater.idle()
