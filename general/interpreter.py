from models.schedule_creator import Schedule, create_schedule, HM_TEMPLATE, replace_schedule
from datetime import datetime


# Реализована бизнес логика
class Interpreter:
    command: str
    operator: str
    subject: str
    meta: [str]
    error = None
    operators = ['измени', 'поменяй', 'завтрак', 'расписание']
    response: str or None

    def parse(self, command: str, schedule: Schedule):
        self.command = command.lower()
        command_split = self.command.split(' ')
        command_width = len(command_split)

        # Пустая команда
        if command_width == 0:
            self.error = 'Пустая команда.'

        # Если команда не пустая
        if command_width >= 1:
            self.operator = command_split[0]

        # Однословные команды
        if command_width == 1:
            if self.operator == 'расписание':
                self.response = create_schedule(schedule)
            elif self.operator == 'завтрак':
                schedule.__init__()
                self.response = 'Расписание на сегодня инициализировано!)'
            else:
                self.response = None
                self.error = 'Команда не распознана.'

        # Команда в 2 слова или больше, работает base_distribution
        if command_width >= 2:
            self.subject = command_split[1]
            self.meta = command.split(' ')[2:]
            if self.meta is str:
                self.meta = [self.meta]
            # Команда длиннее 2 слов
            if command_width > 2:
                if '\n' in command:
                    # Все после первого переноса строки идет последним элементом в качестве title
                    self.meta = [command.split('\n')[0].split(' ')[2:], command[command.index('\n') + 1:]]
            self.base_distribution(schedule)

        if self.error is None:
            return self.error
        print(self.__repr__())
        return self.response

    def base_distribution(self, schedule: Schedule):
        match self.operator:
            case 'поменяй':
                begin, total, title = self.meta
                schedule.mod(self.subject, begin, total, title)
                self.response = 'Изменения применены!)'
            case 'измени':
                if len(self.meta) > 1:
                    self.error = f'Слишком много аргументов ({len(self.meta)}), ' \
                                 f'функция _измени_ принимает 2 аргумента:\n' \
                                 f'1. Название пункта (см. /список);\n2. Время окончания, def. now().'
                    return self.error

                # Проверка, передают ли время, если передали, записываем именно его
                if len(self.meta) == 0:
                    self.meta = [datetime.now().strftime(HM_TEMPLATE)]

                if len(self.meta[0]) == 5 and self.meta[0][2] == ':':
                    schedule.stop(sub=self.subject, time_stop=self.meta[0])
                    self.response = replace_schedule(schedule, self.subject)
                else:
                    self.error = 'Неправильный формат времени!'

            case _:
                self.error = f'Нарушен синтаксис\n{self.command}'

    def __repr__(self):
        log = f'INP: {self.command}\n' \
              f'---\n' \
              f'Была вызвана команда {self.operator} со следующими параметрами:\n{self.subject};\n{self.meta}\n' \
              f'---\n'

        if self.error is None:
            return log + f'OUT: {self.response}'
        return log + f'OUT: {self.error}'
