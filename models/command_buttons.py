from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

btn_change = KeyboardButton('/измени')
btn_rewrite = KeyboardButton('/поменяй')
btn_schedule = KeyboardButton('расписание')
btn_jobs_list = KeyboardButton('/список')
btn_commands = KeyboardButton('/команды')


btn_breakfast = KeyboardButton('завтрак')
btn_first_break = KeyboardButton('первый перерыв')
btn_tea_break = KeyboardButton('чай')
btn_movie = KeyboardButton('кино')
btn_presentation = KeyboardButton('изложение')
btn_second_break = KeyboardButton('второй перерыв')
btn_spelling = KeyboardButton('пропись')
btn_dinner = KeyboardButton('обед')
btn_lms = KeyboardButton('лмс')
btn_third_break = KeyboardButton('третий перерыв')
btn_reading = KeyboardButton('чтение')

# btn_jobs = [btn_breakfast, btn_first_break, btn_first_break, btn_movie, btn_presentation, btn_second_break,
#             btn_spelling, btn_dinner, btn_lms, btn_third_break, btn_reading]

# В диалоговом меню Команды
markup_commands = ReplyKeyboardMarkup().add(
    btn_change).add(btn_rewrite).add(btn_schedule)

# В диалоговом меню Измени/Поменяй
markup_listen = ReplyKeyboardMarkup().add(btn_jobs_list).add(btn_commands)


markup4 = ReplyKeyboardMarkup().row(
    btn_change, btn_rewrite, btn_schedule
)

markup_jobs = ReplyKeyboardMarkup().row(
    btn_breakfast, btn_first_break, btn_tea_break
).row(
    btn_movie, btn_presentation, btn_second_break
).row(
    btn_spelling, btn_dinner, btn_lms
).row(
    btn_third_break, btn_reading
).row(
    btn_commands, btn_schedule
)
