from configparser import ConfigParser
import requests


def get_config():
    config = ConfigParser()
    config.read("user.ini")
    return {
        "api_id": int(config.get("DEFAULT", "api_id")),
        "api_hash": config.get("DEFAULT", "api_hash"),
        "session_name": config.get("DEFAULT", "session"),
        "folders": config.get("DEFAULT", "folders").replace(" ", "").split(","),
    }


URL = "http://127.0.0.1:8000"
SPAM_URL = URL + "/spam/"
FILE = URL + "/file/"


def main():
    request = requests.post(SPAM_URL, json={"text": "asd", **get_config()})
    print(request.json())


if __name__ == "__main__":
    main()
