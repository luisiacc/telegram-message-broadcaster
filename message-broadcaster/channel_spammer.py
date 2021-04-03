from configparser import ConfigParser
from pathlib import Path

from telethon import TelegramClient
from telethon.hints import EntityLike
from telethon.tl import functions


def get_config():
    config = ConfigParser()
    config.read("user.ini")
    return {
        "api_id": int(config.get("DEFAULT", "api_id")),
        "api_hash": config.get("DEFAULT", "api_hash"),
        "session": config.get("DEFAULT", "session"),
        "folders": config.get("DEFAULT", "folders").replace(" ", "").split(","),
        "message_treshold": int(config.get("DEFAULT", "message_treshold")),
    }


config = get_config()
API_ID = config.get("api_id", -1)
API_HASH = config.get("api_hash", "")
SESSION = config.get("session", "")
FOLDERS = config.get("folders", [])
MESSAGE_TRESHOLD = config.get("message_treshold", 10)

assert API_ID != -1, "api_id not provided"
assert API_HASH != "", "api_hash not provided"
assert SESSION != "", "session_name not provided"


class Folder:
    def __init__(self, name) -> None:
        self.path = Path.cwd() / name
        self.image = self.path / "foto.jpg"

        text_path = self.path / "texto.txt"
        self.text = text_path.read_text(encoding="utf-8")


class Spammer:
    def __init__(self, session_name: str, api_id: int, api_hash: str, folders: list) -> None:
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.folders = folders
        self.client = TelegramClient(session_name, api_id, api_hash)

        self.channels_succeed = []
        self.channels_fails = []

    async def get_channels(self) -> list[str]:
        folder_channels_ids = []
        request = await self.client(functions.messages.GetDialogFiltersRequest())
        for dialog_filter in request:
            dialog_dict = dialog_filter.to_dict()
            if dialog_dict.get("title") in self.folders:
                folder_channels_ids.extend(item.get("channel_id") for item in dialog_dict.get("include_peers", []))

        return folder_channels_ids

    async def spam(self, photo, text):
        print(" :O Cargando todos los dialogos para tenerlos ahi por si acaso")
        # this part is important because it fills the entity cache
        await self.client.get_dialogs()
        print(" :X Termine de cargar los dialogos, vamo a darle fuego ya.")

        print("\n ** Comienza lo bueno ahora, empezamos a tirar mensajes.\n")
        for telegram_folder in self.folders:
            folder_channels_ids = await self.get_channels()
            for channel_id in folder_channels_ids:
                channel: EntityLike = await self.client.get_entity(channel_id)
                messages = await self.client.get_messages(channel, limit=MESSAGE_TRESHOLD)
                print(f" (...) Estoy enviando el mensaje al grupo '{channel.title}'")
                if await self.find_myself_in_messages(messages):
                    print(
                        " (.^.) Me convierto en el grillo saltarin para saltar este grupo y no postear para "
                        "que no me baneen :), te falta calle bro\n"
                    )
                    continue
                try:
                    await self.client.send_file(channel_id, photo, caption=text)
                    print(f" (<X>) Termine de enviar el mensaje al grupo - {channel.title} -\n")
                    self.channels_succeed.append(channel.title)
                except Exception as e:
                    self.channels_fails.append(channel.title)
                    print(f" (XXX) Hubo un error enviando el mensaje a este grupo, '{e}'")

    async def find_myself_in_messages(self, messages) -> bool:
        me = await self.client.get_me()
        for msg in messages:
            if msg.from_id.user_id == me.id:
                return True
        return False

    def run(self, photo, text):
        with self.client:
            self.client.loop.run_until_complete(self.spam(photo, text))


def main():
    folder = Folder(input("Pokemon dime el nombre de la carpeta: "))
    spammer = Spammer(SESSION, API_ID, API_HASH, FOLDERS)
    spammer.run(str(folder.image), folder.text)


if __name__ == "__main__":
    main()
