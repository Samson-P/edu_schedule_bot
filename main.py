import configparser
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging
from models.schedule_creator import create_schedule, Schedule, HM_TEMPLATE, replace_schedule, jobs_list, ITEMS
from datetime import datetime
from models.command_buttons import markup_commands, markup_listen, markup_jobs
from models.rewrite_templates import create_rewrite_templ
from general.interpreter import Interpreter


interpreter = Interpreter()

# Открываем файл конфигурации по умолчанию
token_config = configparser.ConfigParser()
token_config.read("static/config/token.ini")
# Имя файла бд и название таблицы берем из конфига
token = token_config['Telegram']['token']

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)
schedule = Schedule()

#
good_boy = 'ок', 'оки', 'хорошо', 'молодец', 'сяб', 'спасибо', 'семки', 'класс', 'кк', 'сеньк', 'збс', 'спс', 'кайф'


@dp.message_handler(commands=['команды'])
async def process_hi3_command(message: types.Message):
    await message.reply("Добавил тебе кнопок с командами, проверяй!)", reply_markup=markup_commands)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привет!\nЯ edu_schedule_bot для малого.\n\nPowered by Samson-P.")


@dp.message_handler(commands=['измени'])
async def send_info_change(message: types.Message):
    await message.reply("Обрати внимание! Функция пишется таким образом:", reply_markup=markup_listen)
    await message.answer("измени <b>название</b>\nили\nизмени <b>название</b> <i>время</i>",
                         parse_mode='HTML')
    await message.answer("Пример:\nИзмени лмс 16:45\n* При этом 16:45 — время окончания.\n"
                         "* А 'лмс' — род деятельности (см. /список).\n"
                         "* Писать можно как с прописной так и с заглавной.")


@dp.message_handler(commands=['поменяй'])
async def send_info_rewrite(message: types.Message):
    await message.reply("Обрати внимание! Функция пишется таким образом:", reply_markup=markup_jobs)
    await message.answer("поменяй <b>название</b> <i>время начала</i> <b>продолжительность</b>\n"
                         "<b>Задание</b>",
                         parse_mode='HTML')
    await message.answer("Пример:\nПоменяй лмс 16:30 60\nРешение задач на скорость.")
    await message.answer("Глянь, я добавил тебе кнопок, выбери пункт, который хочешь изменить и нажми соотв. кнопку, "
                         "отправлю тебе шаблон;)")


@dp.message_handler(commands=['список'])
async def send_info_jobs_list(message: types.Message):
    await message.reply(jobs_list(), reply_markup=markup_commands)


@dp.message_handler(commands=['завтрак'])
async def schedule_init(message: types.Message):
    """
    This handler will be called when user initialize schedule
    """
    schedule.__init__()
    await message.reply(create_schedule(schedule))


@dp.message_handler(commands=['schedule', 'расписание'])
async def schedule_send(message: types.Message):
    """
    This handler will be called when user sends `/schedule`
    """
    await message.reply(create_schedule(schedule), parse_mode='HTML')


@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    if msg.text.lower() == 'привет':
        await msg.answer('Привет!')
    # Обращения к интерпретатору
    elif msg.text.lower() == 'завтрак':
        await msg.answer(interpreter.parse(msg.text.lower(), schedule))

    elif msg.text.lower() == 'расписание':
        await msg.answer(interpreter.parse(msg.text.lower(), schedule))

    elif 'поменяй' in msg.text.lower() or 'измени' in msg.text.lower():
        try:
            cmd = msg.text.lower().split(' ')
            await msg.answer(interpreter.parse(msg.text.lower(), schedule))
            try:
                await msg.answer(interpreter.parse(msg.text.lower(), schedule))
            except BaseException:
                await msg.answer('Что-то не то, попробуй снова.')
        except BaseException:
            await msg.answer('Ты уверен, что оно именно так пишется?')
    # Ответ на случай благодарностей
    elif set(good_boy).intersection(msg.text.lower().split(' ')):
        await msg.answer('Рад был помочь, комрад!')
    # Ответ на нерегламентированные запросы.
    elif len(msg.text.split(' ')) == 1 and msg.text.lower() in ITEMS:
        sub = msg.text.lower()
        await msg.answer(create_rewrite_templ(sub))
    else:
        await msg.answer('Не понимаю, что это значит.')


if __name__ == "__main__":
    executor.start_polling(dp)
