from telethon.tl.custom import Conversation
from typing import Any, Dict, Iterator
from telethon.tl.custom import Message
from telethon import events
from os.path import exists
import json


class JsonFile:
    """ Helper class for dealing with json files """

    def __init__(self, path: str, default_value: Dict[str, Any]):
        self._path = path
        self._readFile(self._path, default_value)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any):
        self._data[key] = value

    def __getattr__(self, name: str) -> Any:
        return getattr(self._data, name)

    def __iter__(self) -> Iterator:
        return iter(self._data)

    def _readFile(self, path: str, default_value: Dict[str, Any]):
        if not exists(path):
            self._saveFile(path, default_value)

        with open(path, "r", encoding="utf-8") as file:
            self._data = json.load(file)

    def _saveFile(self, path: str, data: Dict[str, Any]):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, default=str)

    def save(self):
        """ Saves the internal (modified?) data into the file path that were passed to the __init__. """
        self._saveFile(self._path, self._data)

def callback_for_specific_message(conv: Conversation, message: Message) -> events.CallbackQuery:
    return events.CallbackQuery(chats=[conv.chat_id], func=lambda e: e.message_id==message.id)
