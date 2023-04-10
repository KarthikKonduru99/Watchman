from typing import List, Any

from aw_core.config import load_config_toml
from aw_core.log import setup_logging
import logging
import configparser
from genericpath import isfile
import os
import pickle

logger = logging.getLogger(__name__)

from aw_core import dirs
import sqlite3

# data_dir = dirs.get_data_dir("aw-server")
# filename = 'peewee-sqlite.v2.db'
# filepath = os.path.join(data_dir, filename)
# DB = filepath

#
# def get_token():
#     """ Gets the token from the sqlite3 DB """
#     try:
#         conn = sqlite3.connect(DB)
#         db = conn.cursor()
#         pick = db.execute("select token from authorization").fetchone()
#         token = pickle.loads(pick[0])
#         return token
#     except Exception as e:
#         logger.error("Exception :{}".format(e))
#     finally:
#         conn.commit()
#         conn.close()

# def get_config():
#     """ Requests user config from the server and returns the user configuration and time in seconds """
#     hdr = {'Authorization': 'Bearer {}'.format(get_token())}
#     js = {"username": os.getlogin()}
#     response = requests.post('link', headers=hdr, json=js)
#     return user_config(response.json())


# try:
#     conn = sqlite3.connect(DB)
#     cur = conn.cursor()
#     query = 'CREATE TABLE IF NOT EXISTS config (id INTEGER PRIMARY KEY AUTOINCREMENT, );'
#     cur.execute(query)
#     config = get_config()
#
# except:
#     pass


# ----- CREATION CONFIG.INI TO CONFIGURATION ----- #

# logger.info("Setting Config file...")
# path = os.getcwd() + '\config.ini'
# my_config_parser = configparser.ConfigParser()

# try:
#     if os.path.isfile(path):
#         logger.info("Config file found getting server settings")
#         my_config_parser.read('config.ini')
#         server = my_config_parser.get('SETTINGS', 'SERVER')
#         event_delay = my_config_parser.get('SETTINGS','EVENT_DELAY')
#         logger.info(f"Server Name is : {server}",f"Event Delay is : {event_delay}")
#     else:
#         logger.info("Config not found setting default config")
#         server = 'demo.cxparadise.com'
#         event_delay = 60
#         my_config_parser.add_section('SETTINGS')
#         my_config_parser.set('SETTINGS','; Any values can be changed, Please restart your machine after changes.')
#         my_config_parser.set('SETTINGS','; SERVER','; Default is demo.cxparadise.com')
#         my_config_parser.set('SETTINGS', 'SERVER', f'{server}')
#         my_config_parser.set('SETTINGS','; EVENT_DELAY','; Default is set for 60 Seconds')
#         my_config_parser.set('SETTINGS','EVENT_DELAY',f'{event_delay}')
#
#         my_config_parser.add_section('DATABASE')
#         my_config_parser.set('DATABASE','; Table_name_for_afk','; ')
#
#         with open(path, 'w') as file:
#             my_config_parser.write(file)
# except Exception as e:
#     logger.info('Exception : {}'.format(e))
#
# logger.info(f"Server INFO : {server}")
# logger.info(f"Event delay is set to : {event_delay} seconds.")

# ------------------ END OF CONFIG.INI LOGC ------------------ #


default_config = """
[aw-qt]
autostart_modules = ["aw-server", "aw-watcher-afk", "aw-watcher-window"]

[aw-qt-testing]
autostart_modules = ["aw-server", "aw-watcher-afk", "aw-watcher-window"]
""".strip()

class AwQtSettings:
    def __init__(self, testing: bool):
        """
        An instance of loaded settings, containing a list of modules to autostart.
        Constructor takes a `testing` boolean as an argument
        """
        config = load_config_toml("aw-qt", default_config)
        config_section: Any = config["aw-qt" if not testing else "aw-qt-testing"]
        self.autostart_modules: List[str] = config_section["autostart_modules"]
