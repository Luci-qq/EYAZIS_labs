import asyncio
import sys
import g4f
from g4f.client import Client

if sys.platform == 'win64':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

MODEL = g4f.models.gpt_4_turbo

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



def get_synonyms(word: str):
    client = Client(metaclass=Singleton)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"Напиши синонимы слову {word} в виде строки разделяя запятой и не пиши ничего лишнего"}],
    )
    return response.choices[0].message.content.split(', ')


def get_antonyms(word: str):
    client = Client(metaclass=Singleton)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"Напиши антонимы слову {word} в виде строки разделяя запятой и не пиши ничего лишнего"}],
    )
    return response.choices[0].message.content.split(', ')

def get_definition(word: str):
    client = Client(metaclass=Singleton)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"Напиши определение для слова {word} и не пиши ничего лишнего, исходное слово не должно быть никак выделено"}],
    )
    return response.choices[0].message.content.split(', ')


def chatting(message: str):
    client = Client(metaclass=Singleton)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"{message}"}],
    )
    return response.choices[0].message.content