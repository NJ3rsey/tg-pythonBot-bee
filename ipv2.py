import sys
import ping3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
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


# функция обратного вызова
def echo(update, context):
    # добавим в начало полученного сообщения строку 'ECHO: '
    text = 'ECHO: ' + update.message.text
    # `update.effective_chat.id` - определяем `id` чата,
    # откуда прилетело сообщение
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def check(update, context):
    try:
        ping3.verbose_ping(context.args[0], count=6, size=1400)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\nВсе хорошо. Хост доступен и отвечает.")
    except ping3.errors.TimeToLiveExpired as err:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=err.ip_header[
                                     "src_addr"])  # TimeToLiveExpired, DestinationUnreachable and DestinationHostUnreachable have ip_header and icmp_header attached.
    except ping3.errors.HostUnknown:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Неизвестный или неверный хост.")
    except ping3.errors.Timeout:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Время запроса истекло, хост недоступен или не отвечает."
                                      "\n(Request timeout for ICMP packet)")
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Хост не указан")
    except AttributeError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Хост не указан")


# FOR TESTING NEEDS ========================================================
def ch(update, context):
    try:
        log.start()
        ping3.verbose_ping(context.args[0], count=6, size=1400)
        log.stop()

        # context.bot.send_message(chat_id=update.effective_chat.id,
        #                         text=log.messages)

        def concat():
            l = log.messages
            print(l[::2])
            # for every in range(len(l)):
            return l

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=concat())

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\nВсе хорошо. Хост доступен и отвечает.")
    except ping3.errors.TimeToLiveExpired as err:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=err.ip_header[
                                     "src_addr"])  # TimeToLiveExpired, DestinationUnreachable and DestinationHostUnreachable have ip_header and icmp_header attached.
    except ping3.errors.HostUnknown:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Неизвестный или неверный хост.")
    except ping3.errors.Timeout:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Время запроса истекло, хост недоступен или не отвечает."
                                      "\n(Request timeout for ICMP packet)")
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Хост не указан")
    except AttributeError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Хост не указан")


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


# Обратите внимание, что из обработчика в функцию
# передаются экземпляры `update` и `context`
def start(update, context):
    # `bot.send_message` это метод Telegram API
    # `update.effective_chat.id` - определяем `id` чата,
    # откуда прилетело сообщение
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="")


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Неизвестная команда.")


class Logger:
    stdout = sys.stdout
    messages = []

    def start(self):
        sys.stdout = self

    def stop(self):
        sys.stdout = self.stdout

    def write(self, text):
        self.messages.append(text)


# logger Class to catch output from ping3 module to trace it to the TG chat
log = Logger()

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
check_handler = CommandHandler('c', check)
# регистрируем обработчик в диспетчере
dispatcher.add_handler(check_handler)

ch_handler = CommandHandler('ch', ch)  # FOR TESING NEEDS
dispatcher.add_handler(ch_handler)  # FOR TESING NEEDS

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# запуск прослушивания сообщений
updater.start_polling()
# обработчик нажатия Ctrl+C
updater.idle()
