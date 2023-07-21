import sqlite3


def get_tester_ids():
    while True:
        tester_ids_input = input(
            "Tester ID'lerini girin (virgülle ayırarak): ")
        tester_ids_str = tester_ids_input.split(",")
        tester_ids = []

        for id_str in tester_ids_str:
            try:
                id_int = int(id_str.strip())
                tester_ids.append(id_int)
            except ValueError:
                print(
                    f"{id_str} geçersiz bir ID. Lütfen yalnızca tamsayıları girin.")

        if tester_ids:
            return tester_ids
        else:
            print("Lütfen en az bir Tester ID girin.")

# Bot Ayarları


try:
    print("Hoşgeldin! İlk olarak bot ayarları ile başlıyoruz.")

    botToken = input("Bot Token: ")
    botName = input("Bot Adı: ")
    botPrefix = input("Bot Prefix: ")
    print(
        f"Bot Prefix'i Devamlı Olarak Aktif Olucaksa Örneğin {botPrefix} merhaba ise 1 sadece merhaba ise 0\nsadece merhaba farklı sunuculardada aktif olucağı için riskler taşır!")
    botPrefixActive = input("Prefix Aktif: ")

    # Kullanıcı Ayarları

    print("Bot ayarlarını bitirdiğimize göre kullanıcı ayarlarına başlayalım!")

    ownerId = input("Sahip ID: ")
    print("Tester IDlerini giriniz 1, 2, 3, 4, 5 gibi")
    testerIds = get_tester_ids()
    afkActive = 0
    afkReason = 0
except Exception as error:
    print("Bir hata oluştu:", error)


# Bot ayarlarını veritabanına kaydetme

def save_bot_settings():
    try:
        connection = sqlite3.connect('bot.sql')
        cursor = connection.cursor()

        # Tablo güncelleme
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_settings (
                id INTEGER PRIMARY KEY,
                botToken TEXT,
                botName TEXT,
                botPrefix TEXT,
                botPrefixActive INTEGER,
                ownerId INTEGER
            )''')

        # Ayarları güncelleme veya ekleme
        cursor.execute('''
            INSERT OR REPLACE INTO bot_settings (id, botToken, botName, botPrefix, botPrefixActive, ownerId)
            VALUES (1, ?, ?, ?, ?, ?)
        ''', (botToken, botName, botPrefix, botPrefixActive, ownerId))

        connection.commit()
        connection.close()
        print("Bot ayarları başarıyla kaydedildi.")
    except sqlite3.Error as error:
        print("Bot ayarlarını kaydederken bir hata oluştu:", error)

# Kullanıcı ayarlarını veritabanından almak


def get_user_settings(user_id):
    connection = sqlite3.connect('bot.sql')
    cursor = connection.cursor()

    # Tablodan kullanıcı ayarlarını almak
    cursor.execute(
        'SELECT afkActive, afkReason FROM user_settings WHERE id=?', (user_id,))
    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None

    afk_active, afk_reason = result
    return {
        'afkActive': afk_active,
        'afkReason': afk_reason
    }

# Kullanıcı ayarlarını veritabanında güncelleme veya ekleme


def update_user_settings(user_id, afk_active, afk_reason):
    try:
        connection = sqlite3.connect('bot.sql')
        cursor = connection.cursor()

        # Tablo oluşturma
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_settings
                          (id INTEGER PRIMARY KEY,
                          afkActive INTEGER,
                          afkReason TEXT)''')

        # Ayarları güncelleme veya ekleme
        cursor.execute('INSERT OR REPLACE INTO user_settings (id, afkActive, afkReason) VALUES (?, ?, ?)',
                       (user_id, afk_active, afk_reason))

        connection.commit()
        connection.close()
        print("Kullanıcı ayarları başarıyla güncellendi.")
    except sqlite3.Error as error:
        print("Kullanıcı ayarlarını güncellerken bir hata oluştu:", error)


print("İşlemler bitti! Görüşmek Üzere :)")

# Bot ayarlarını kaydetme
save_bot_settings()

# Kullanıcı ayarlarını güncelleme veya ekleme
update_user_settings(ownerId, afkActive, afkReason)
for tester_id in testerIds:
    update_user_settings(tester_id, afkActive, afkReason)
