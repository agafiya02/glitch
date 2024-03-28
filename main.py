import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(f"Я получил сообщение {update.message.text}")


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def time(update, context):
    now = datetime.datetime.now()
    await update.message.reply_text(now.strftime('%H:%M'))


async def date(update, context):
    now = datetime.datetime.now()
    await update.message.reply_text(now.strftime("%Y-%m-%d"))


async def set_timer(update, context):
    chat_id = update.effective_message.chat_id
    context.job_queue.run_once(task, update.message.text, chat_id=chat_id, name=str(chat_id), data=update.message.text)

    text = f'Вернусь через 5 с.!'
    await update.effective_message.reply_text(text)


async def task(context):
    """Выводит сообщение"""
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! 5c. прошли!')


def main():
    application = Application.builder().token('7054458633:AAHwiwR67W2uM8cwMssaz2Z6XprvTc9Jf-g').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("time", time))
    application.add_handler(CommandHandler("date", date))
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
