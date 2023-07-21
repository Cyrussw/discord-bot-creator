import sqlite3


def get_bot_settings():
    connection = sqlite3.connect('bot.sql')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM bot_settings')
    result = cursor.fetchone()

    connection.close()

    return result

# Bot Settings


bot_settings = get_bot_settings()

botToken = bot_settings[1]
botName = bot_settings[2]
botPrefix = bot_settings[3]
botPrefixActive = bot_settings[4]
ownerId = bot_settings[5]

# User Settings


def get_user_ids():
    connection = sqlite3.connect('bot.sql')
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM user_settings')
    result = cursor.fetchall()

    connection.close()

    user_ids = [row[0] for row in result]
    return user_ids


# Get Users Id
testerIds = get_user_ids()
