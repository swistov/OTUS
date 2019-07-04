import configparser
import os

settings = os.path.join(os.getcwd(), 'settings.conf')

config = configparser.ConfigParser()
config.read(settings)


try:
    db = config.get('DB_COONECT', 'db')
except configparser.Error:
    db = 'default.db'

try:
    db_path = config.get('DB_COONECT', 'db_path')
    full_path = os.path.join(db_path, db)
except configparser.Error:
    db_path = os.getcwd()
    full_path = os.path.join(db_path, db)

try:
    control_foreign_keys = config.getboolean('DB_COONECT', 'control_foreign_keys')
except configparser.Error:
    control_foreign_keys = False
