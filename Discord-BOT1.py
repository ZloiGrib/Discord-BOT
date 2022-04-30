# Импортируем все нужные нам библиотеки.
import json
import os
import discord
# Импортируем из config settings.
from config import settings


# Берём из списка городов города.
def parse_city_json(json_file='Goroda.json'):
    a = None
    try:
        b = open(json_file, "r", encoding="utf-8")
        a = json.load(b)
    except Exception as err:
        print(err)
        return None
    finally:
        b.close()
        # Получаем чисто список с названиями городов.
    return [city['city'].lower() for city in a]


# Получаеи на вход название города
def get_city(city):
    # Удаляем все ненужные пробелы если они есть и перегоняем всё в нижний регистр //
    # и убираем первый который ввёл пользователь.
    c = city.strip().lower()[1:]
    # Если корректное название города то начинаем цикл.
    if is_correct_city_name(c):
        # Проверка город, совпадает ли последняя буква с первой.
        if get_city.previous_city != "" and c[0] != get_city.previous_city[-1]:
            return 'Город должен начинаться на "{0}"!'.format(get_city.previous_city[-1])
        # Проверяем не называли ли город заранее
        if c not in cities_already_named:
            # Если город попался в первый раз добовляем его в названные города.
            cities_already_named.add(c)
            # Получаем последнюю букву введённого города.
            last_latter_city = c[-1]
            proposed_names = list(filter(lambda x: x[0] == last_latter_city, cities))
            if proposed_names:
                for city in proposed_names:
                    # Города которые уже называл бот.
                    if city not in cities_already_named:
                        # Если бот не называл город, но потом назвал добовляем в список названных городов.
                        cities_already_named.add(city)
                        get_city.previous_city = city
                        # Первы й символ строки заглавный.
                        return city.capitalize()
            return 'Я не знаю города на эту букву. Вы выиграли!'
        else:
            return 'Город уже был назван :(. Повторите попытку.'
    else:
        return 'Некорректное название города. Повторите попытку.'


get_city.previous_city = ""


# Проверка на корректность названий города.
def is_correct_city_name(city):
    # Если последний символ в названии города это буква и //
    # последний символ не мягкий или твёрдый знак значит это город.
    return city[-1].isalpha() and city[-1] not in ('ь', 'ъ')


# Обнуляем уже названные города и подгружаем ещё.
def refresh():
    cities = parse_city_json()[:1000]
    cities_already_named = set()


# города которые знает бот.
cities = parse_city_json()[:1000]
# Города, которые уже называли.
cities_already_named = set()

# Из файла config.py получаем токен.
TOKEN = settings['token']

# Создаём бота.
bot = discord.Client()


@bot.event
# Бот слушает все сообщения который говорит пользователь.
async def on_message(message):
    # Если сообщение пришло от бота, то пропускаем его.
    if message.author == bot.user:
        return
    # Если сообщение пришло не от бота, то проверяем начинается ли оно с мягкого знака.
    if message.content.startswith('!'):
        if message.content == '!refresh':
            refresh()
        else:
            # Бот отправляет ответ.
            response = get_city(message.content)
            await message.channel.send(response)


# Запуск бота.
bot.run(TOKEN)
