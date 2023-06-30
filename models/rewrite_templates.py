from models.schedule_creator import ITEMS
from datetime import datetime


items_templ = {
    'завтрак': ' завтрак _ _\nОвсянка, сэр!',
    'первый': ' первый _ _',
    'чай': ' чай _ _',
    'кино': ' кино _ _',
    'изложение': ' изложение _ _\nИзложение в формате MS Word по просмотренному фильму.',
    'второй': ' второй _ _',
    'пропись': ' пропись _ _\nСлова для прописи в рабочей тетради.',
    'обед': ' обед _ _',
    'лмс': ' лмс _ _\nLMS Chamilo Арифметика > Tests > {}',
    'третий': ' перерыв _ _',
    'чтение': ' чтение _ _\nАлиса в стране чудес, 20 стр.'
}


def create_rewrite_templ(sub):
    if sub not in ITEMS:
        return 'Что-то не так... Попробуй еще раз.'

    match sub:
        case 'лмс':
            return 'поменяй' + items_templ[sub].format(datetime.now().strftime("%d%m%Y"))
        case _:
            return 'поменяй' + items_templ[sub]

