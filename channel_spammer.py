from configparser import ConfigParser
from pathlib import Path

from telethon import TelegramClient
from telethon.tl import functions


def get_config():
    config = ConfigParser()
    config.read("user.ini")
    return {
        "api_id": int(config.get("DEFAULT", "api_id")),
        "api_hash": config.get("DEFAULT", "api_hash"),
        "session": config.get("DEFAULT", "session"),
        "folders": config.get("DEFAULT", "folders").replace(" ", "").split(","),
    }


config = get_config()
api_id = config.get("api_id", -1)
api_hash = config.get("api_hash", "")
session_name = config.get("session", "")

assert api_id != -1, "api_id not provided"
assert api_hash != "", "api_hash not provided"
assert session_name != "", "session_name not provided"

client = TelegramClient(session_name, api_id, api_hash)


class Folder:
    def __init__(self, name) -> None:
        self.path = Path.cwd() / name
        self.image = self.path / "foto.jpg"

        text_path = self.path / "texto.txt"
        self.text = text_path.read_text(encoding="utf-8")


async def get_channels_on_folder(folder_name):
    folder_channels_ids = []
    request = await client(functions.messages.GetDialogFiltersRequest())
    for dialog_filter in request:
        dialog_dict = dialog_filter.to_dict()
        if dialog_dict.get("title") == folder_name:
            folder_channels_ids.extend(item.get("channel_id") for item in dialog_dict.get("include_peers", []))

    return folder_channels_ids


async def main(folder_name):
    folder = Folder(folder_name)

    print(" :O Cargando todos los dialogos para tenerlos ahi por si acaso")
    # this part is important because it fills the entity cache
    await client.get_dialogs()
    print(" :X Termine de cargar los dialogos, vamo a darle fuego ya.")

    print("\n ** Comienza lo bueno ahora, empezamos a tirar mensajes.\n")
    for telegram_folder in config.get("folders"):
        folder_channels_ids = await get_channels_on_folder(telegram_folder)
        for channel_id in folder_channels_ids:
            channel = await client.get_entity(channel_id)
            print(f" (...) Estoy enviando el mensaje al grupo '{channel.title}'")
            await client.send_file(channel_id, str(folder.image), caption=folder.text)
            print(f" (<X>) Termine de enviar el mensaje al grupo - {channel.title} -\n")


if __name__ == "__main__":
    folder_name = input("Pokemon dime el nombre de la carpeta: ")
    assert bool(folder_name.strip()), "folder_name not provided"
    with client:
        client.loop.run_until_complete(main(folder_name))
