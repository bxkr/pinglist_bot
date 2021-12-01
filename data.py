import json
import os
from aiogram.types import Message


def _get_data() -> dict:
    return json.load(open('data.json'))


def chat_m(message: Message) -> None:
    chat = str(message.chat.id)
    if not os.path.exists('data.json'):
        json.dump({}, open('data.json', 'w'))
    data = _get_data()
    if chat not in data.keys():
        data[chat] = {}
    json.dump(data, open('data.json', 'w'))


def get_groups(message: Message) -> dict:
    data = _get_data()
    return {i: v for i, v in zip(range(len(data[str(message.chat.id)])), list(data[str(message.chat.id)].keys()))}


def get_group_members(message: Message, index: int) -> list:
    data = _get_data()
    return data[str(message.chat.id)][list(data[str(message.chat.id)].keys())[index]]


def add_group(message: Message, name: str, members: list) -> None:
    current_data = _get_data()
    new_data: dict = current_data.copy()
    new_data[str(message.chat.id)][name] = members
    json.dump(new_data, open('data.json', 'w'))


def add_to_group(message: Message, index: int, new_members: list) -> None:
    current_data = _get_data()
    new_data: dict = current_data.copy()
    new_data[str(message.chat.id)][list(new_data[str(message.chat.id)].keys())[index]] += new_members
    json.dump(new_data, open('data.json', 'w'))


def remove_group(message: Message, index: int):
    current_data = _get_data()
    new_data: dict = current_data.copy()
    del new_data[str(message.chat.id)][list(new_data[str(message.chat.id)].keys())[index]]
    json.dump(new_data, open('data.json', 'w'))


def remove_from_group(message: Message, index: int, username: str) -> None:
    current_data = _get_data()
    new_data: dict = current_data.copy()
    del new_data[str(message.chat.id)][
        list(new_data[str(message.chat.id)].keys())[index]][
        new_data[str(message.chat.id)][list(new_data[str(message.chat.id)].keys())[index]].index(username)
    ]
    json.dump(new_data, open('data.json', 'w'))
