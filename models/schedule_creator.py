from jinja2 import Template
from datetime import datetime, timedelta

HM_TEMPLATE = '%H:%M'

ITEMS = [
    'завтрак', 'первый', 'чай', 'кино',
    'изложение', 'второй', 'пропись', 'обед',
    'лмс', 'третий', 'чтение'
]


items_mod = {
    'завтрак': 'breakfast',
    'первый': 'first_brake',
    'чай': 'tea_brake',
    'кино': 'movie',
    'изложение': 'presentation',
    'второй': 'second_break',
    'пропись': 'spelling',
    'обед': 'dinner',
    'лмс': 'lms',
    'третий': 'third_break',
    'чтение': 'reading'
}


BREAKFAST_TIMEDELTA = 45
BREAKFAST_LOGO = 'Овсянка, сэр!'

FIRST_BRAKE_TIMEDELTA = 20

TEA_BRAKE_TIMEDELTA = 30

MOVIE_LINK = 'https://www.culture.ru/live/cinema/movies/family/child-100'
MOVIE_TIMEDELTA = 60
MOVIE_LOGO = 'ХФ "Не Горюй!"'

PRESENTATION_TIMEDELTA = 70
PRESENTATION_LOGO = 'Изложение по просмотренному фильму в формате MS Word.'

SECOND_BRAKE_TIMEDELTA = 30

SPELLING_TIMEDELTA = 25
SPELLING_LOGO = 'Пропись по заданию.'

DINNER_TIMEDELTA = 60
DINNER_LOGO = 'Обед.'

LMS_TIMEDELTA = 180
LMS_LOGO = 'Решение задач в Chamilo LMS + перерывы'

THIRD_BRAKE_TIMEDELTA = 90

READING_LOGO = 'Чтение 20 страниц. "Алиса в стране чудес"'
READING_TIMEDELTA = 40


def calc(before: str, delta: int):
    return (datetime.strptime(before, HM_TEMPLATE) + timedelta(minutes=delta)).strftime(HM_TEMPLATE)


class Schedule:
    today = datetime.now().strftime('%d%m%Y')

    def __init__(self):
        self.breakfast = self.Item('Завтрак', total=BREAKFAST_TIMEDELTA)
        self.first_brake = self.Item('Первый перерыв', total=FIRST_BRAKE_TIMEDELTA, before_end=self.breakfast.end)
        self.tea_brake = self.Item('Чай, можно с халвой', total=TEA_BRAKE_TIMEDELTA, before_end=self.first_brake.end)
        self.movie = self.Movie(MOVIE_LOGO, total=MOVIE_TIMEDELTA, before_end=self.tea_brake.end, movie_link=MOVIE_LINK)
        self.presentation = self.Item(PRESENTATION_LOGO, total=PRESENTATION_TIMEDELTA, before_end=self.movie.end)
        self.second_break = self.Item('Второй перерыв', total=SECOND_BRAKE_TIMEDELTA, before_end=self.presentation.end)
        self.spelling = self.Item(SPELLING_LOGO, total=SPELLING_TIMEDELTA, before_end=self.second_break.end)
        self.dinner = self.Item(DINNER_LOGO, total=DINNER_TIMEDELTA, before_end=self.spelling.end)
        self.lms = self.Item(LMS_LOGO, total=LMS_TIMEDELTA, before_end=self.dinner.end)
        self.third_break = self.Item('Третий перерыв', total=THIRD_BRAKE_TIMEDELTA, before_end=self.lms.end)
        self.reading = self.Item(READING_LOGO, total=READING_TIMEDELTA, before_end=self.third_break.end)

    def stop(self, sub, time_stop, time_start=None, mode=None):
        match sub:
            case 'завтрак':
                self.breakfast.end = time_stop
            case 'первый':
                self.first_brake.end = time_stop
            case 'чай':
                self.tea_brake.end = time_stop
            case 'кино':
                self.movie.end = time_stop
            case 'изложение':
                self.presentation.end = time_stop
            case 'второй':
                self.second_break.end = time_stop
            case 'пропись':
                self.spelling.end = time_stop
            case 'обед':
                self.dinner.end = time_stop
            case 'лмс':
                self.lms.end = time_stop
            case 'третий':
                self.third_break.end = time_stop
            case 'чтение':
                self.reading.end = time_stop
            case _:
                pass

    def mod(self, sub, begin, total, title, link=None):
        sub_object = getattr(self, items_mod[sub])
        sub_object.title = title
        sub_object.begin = begin
        sub_object.total = int(total)
        sub_object.end = calc(begin, int(total))
        if link is not None:
            if hasattr(sub_object, 'link'):
                sub_object.link = link
        self.replace(sub)

    def replace(self, sub):
        if sub in ITEMS:
            rep_items = ITEMS[ITEMS.index(sub) + 1:len(ITEMS)]
            if 'завтрак' in rep_items:
                self.breakfast = self.Item('Завтрак', total=BREAKFAST_TIMEDELTA)
            if 'первый' in rep_items:
                self.first_brake = self.Item('Первый перерыв', total=FIRST_BRAKE_TIMEDELTA,
                                             before_end=self.breakfast.end)
            if 'чай' in rep_items:
                self.tea_brake = self.Item('Чай, можно с халвой', total=TEA_BRAKE_TIMEDELTA,
                                           before_end=self.first_brake.end)
            if 'кино' in rep_items:
                self.movie = self.Movie(MOVIE_LOGO, total=MOVIE_TIMEDELTA, before_end=self.tea_brake.end,
                                        movie_link=MOVIE_LINK)
            if 'изложение' in rep_items:
                self.presentation = self.Item(PRESENTATION_LOGO, total=PRESENTATION_TIMEDELTA,
                                              before_end=self.movie.end)
            if 'второй' in rep_items:
                self.second_break = self.Item('Второй перерыв', total=SECOND_BRAKE_TIMEDELTA,
                                              before_end=self.presentation.end)
            if 'пропись' in rep_items:
                self.spelling = self.Item(SPELLING_LOGO, total=SPELLING_TIMEDELTA, before_end=self.second_break.end)
            if 'обед' in rep_items:
                self.dinner = self.Item(DINNER_LOGO, total=DINNER_TIMEDELTA, before_end=self.spelling.end)
            if 'лмс' in rep_items:
                self.lms = self.Item(LMS_LOGO, total=LMS_TIMEDELTA, before_end=self.dinner.end)
            if 'третий' in rep_items:
                self.third_break = self.Item('Третий перерыв', total=THIRD_BRAKE_TIMEDELTA, before_end=self.lms.end)
            if 'чтение' in rep_items:
                self.reading = self.Item(READING_LOGO, total=READING_TIMEDELTA, before_end=self.third_break.end)

    class Item:
        """
        title
        total
        begin
        end
        """
        def __init__(self, title, total: int, before_end: str = datetime.now().strftime(HM_TEMPLATE)):
            self.title = title
            self.total = total
            self.begin = before_end
            self.end = calc(before_end, total)

        def time(self):
            return f'{self.begin} — {self.end}'

        def __repr__(self):
            return self.title

    class Movie(Item):
        """
        movie: name of film
        movie_time
        movie_total: duration of minutes
        movie_link
        """

        def __init__(self, movie: str, total: int, before_end: str,  movie_link: str):
            super().__init__(movie, total, before_end)
            self.link = movie_link

        def __repr__(self):
            return self.title


def create_schedule(schedule):
    filename = 'static/schedule_templates/schedule.templ'
    txt = ''
    with open(filename, mode='r', encoding='utf_8') as file:
        txt += file.read()

    content = {'schedule': schedule}
    return Template(txt).render(content)


def jobs_list():
    filename = 'static/schedule_templates/jobs_list.templ'
    txt = ''
    with open(filename, mode='r', encoding='utf_8') as file:
        txt += file.read()
    return txt


def replace_schedule(schedule, sub):
    if sub not in ITEMS:
        return f'Нет такого "{sub}"!'

    filename = f'static/schedule_templates/schedule_{ITEMS.index(sub) + 1}.templ'
    if sub == 'лмс':
        filename = f'static/schedule_templates/schedule_9-12.templ'

    txt = ''
    with open(filename, mode='r', encoding='utf_8') as file:
        txt += file.read()

    content = {'schedule': schedule}
    return Template(txt).render(content)


if __name__ == "__main__":
    pass
