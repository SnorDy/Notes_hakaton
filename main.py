# импортируем библиотеки
from flask import Flask, request, jsonify
from random import choice
import logging

# создаём приложение
# мы передаём __name__, в нём содержится информация,
# в каком модуле мы находимся.
# В данном случае там содержится '__main__',
# так как мы обращаемся к переменной из запущенного модуля.
# если бы такое обращение, например, произошло внутри модуля logging,
# то мы бы получили 'logging'
app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# Создадим словарь, чтобы для каждой сессии общения
# с навыком хранились подсказки, которые видел пользователь.
# Это поможет нам немного разнообразить подсказки ответов
# (buttons в JSON ответа).
# Когда новый пользователь напишет нашему навыку,
# то мы сохраним в этот словарь запись формата
# sessionStorage[user_id] = {'suggests': ["Не хочу.", "Не буду.", "Отстань!" ]}
# Такая запись говорит, что мы показали пользователю эти три подсказки.
# Когда он откажется купить слона,
# то мы уберем одну подсказку. Как будто что-то меняется :)
sessionStorage = {}


@app.route('/', methods=['POST'])
# Функция получает тело запроса и возвращает ответ.
# Внутри функции доступен request.json - это JSON,
# который отправила нам Алиса в запросе POST

def main():
    logging.info(f'Request: {request.json!r}')  # логирование

    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    req = request.json  # получаем запрос пользователя из навыка
    if req['session']['new']:  # если сессия новая, то выводим приветственное сообщение
        response['response']['text'] = 'Добро пожаловать в навык "Умные заметки"! ' \
                                       'Я помогу вам сохранять ваши записи и события, чтобы вы о них не забыли.' \
                                       'Что вы хотите сделать сейчас?'
        response['response']['buttons'] = [{'title': 'Добавить заметку', 'hide': True},
                                           # добавление кнопок для выбора действия
                                           {'title': 'Выход', 'hide': False},
                                           {'title': 'Редактировать заметку', 'hide': True},
                                           {'title': 'Удалить заметку', 'hide': True},
                                           {'title': 'Добавить событие', 'hide': True},
                                           {'title': 'Редактировать событие', 'hide': True},
                                           {'title': 'Удалить событие', 'hide': True}]
    else:  # если нет, то проверяем  ключевые слова в сообщении
        if req['request']['original_utterance'].lower() in ['добавить заметку', 'создать заметку']:
            add_note(response)
        elif req['request']['original_utterance'].lower() in ['удалить заметку']:
            delete_note(response)
        elif req['request']['original_utterance'].lower() in ['выйти', 'выход', 'пока', 'до свидания', 'прощай',
                                                              'закончить', 'стоп']:
            farewells = ['До новых встреч!', 'Пока!', 'До свидания!']
            response['response']['text'] = choice(farewells)
            response['response']['end_session'] = True

        else:
            response['response']['text'] = 'Извините, я вас не понимаю!'
    return jsonify(response)


def choice_func(response):  # функция выбора, вызывается после каждого действия пользователя
    response['response']['text'] += 'Что ещё вы хотите сделать?'
    response['response']['buttons'] = [{'title': 'Добавить заметку', 'hide': True},
                                       {'title': 'Выход', 'hide': False},
                                       {'title': 'Редактировать заметку', 'hide': True},
                                       {'title': 'Удалить заметку', 'hide': True},
                                       {'title': 'Добавить событие', 'hide': True},
                                       {'title': 'Редактировать событие', 'hide': True},
                                       {'title': 'Удалить событие', 'hide': True}]


def add_note(response):  # добавление заметки
    response['response']['text'] = 'Заметка успешно создана! '
    choice_func(response)
    return response


def delete_note(response):  # удаление заметки
    response['response']['text'] = 'Заметка успешно удалена. '
    choice_func(response)


def change_note_title(response, title):  # изменение названия заметки
    pass


def add_event(response):
    response['response']['text'] = 'Событие {event_title} добавлено! '


def delete_event(response):
    response['response']['text'] = 'Событие {event_title} удалено из вашего списка задач!'


def change_event_time(response, time):
    response['response']['text'] = 'Время события {event_title} изменено на {time}. '


def change_event_desc(response, description):
    response['response']['text'] = 'Описание события {event_title} изменено. '


if __name__ == '__main__':
    app.run()
