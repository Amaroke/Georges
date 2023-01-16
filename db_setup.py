import mysql.connector
import configparser

config = configparser.RawConfigParser()
config.read('config.ini')
db_name = config.get('settings', 'database')

db = mysql.connector.connect(
    host=config.get('settings', 'host'),
    user=config.get('settings', 'username'),
    passwd=config.get('settings', 'password'),
)

cursor = db.cursor()

cursor.execute("CREATE DATABASE db_name")

db.close()
