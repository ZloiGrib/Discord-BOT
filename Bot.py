import json
import os
import discord
from config import settings


# os.chdir('/home/peoples/discord-bot')

def parse_city_json(json_file='Goroda.json'):
    a = None
    try:
        b = open(json_file, "r", encoding="utf-8")
        # Преобразуем объект b в файл Python
        a = json.load(b)
    except Exception as err:
        print(err)
        return None
    finally:
        b.close()
        # Получаем список с названиями городов
    return [city['city'].lower() for city in a]


# Получаем название города
def get_city(city):
    # Убираем все не нужные пробелы и переводим всё в нижний регистр
    c = city.strip().lower()[1:]
    # Если название города корректно то переходим в цикл
    if is_correct_city_name(c):
        # Проверка на корректность
        if get_city.previous_city != "" and c[0] != get_city.previous_city[-1]:
            return 'Город должен начинаться на "{0}"!'.format(get_city.previous_city[-1])
        # Проверка не называли ли город заранее
        if c not in cities_already_named:
            cities_already_named.add(c)
            # Последняя буква названного города
            last_latter_city = c[-1]
            # Отбираем те города у которых первая и последняя буквы совпадают
            proposed_names = list(filter(lambda x: x[0] == last_latter_city, cities))
            if proposed_names:
                for city in proposed_names:
                    if city not in cities_already_named:
                        cities_already_named.add(city)
                        get_city.previous_city = city
                        return city.capitalize()
            return 'Я не знаю города на эту букву. Ты выиграл'
        else:
            return 'Город уже был. Повторите попытку'
    else:
        return 'Некорректное название города. Повторите попытку'


# Статическая переменная функции, то есть предыдущий город
get_city.previous_city = ""


# Проверка на корректность
def is_correct_city_name(city):
    return city[-1].isalpha() and city[-1] not in ('ь', 'ъ')


def refresh():
    cities = parse_city_json()[:1000]
    cities_already_named = set()


# города которые знает бот
cities = parse_city_json()[:1000]
# города, которые уже называли
cities_already_named = set()

TOKEN = settings['token']

bot = discord.Client()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!'):
        if message.content == '!refresh':
            refresh()
        else:
            response = get_city(message.content)
            await message.channel.send(response)


bot.run(TOKEN)
