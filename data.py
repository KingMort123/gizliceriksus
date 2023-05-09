import sqlite3
# slot.db adında bir veritabanı dosyası oluşturuyoruz
conn = sqlite3.connect("slot.db")
# Bir cursor nesnesi alıyoruz
cur = conn.cursor()
# users adında bir tablo oluşturuyoruz
# Bu tabloda id (INTEGER), money (INTEGER) sütunları var
cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, money INTEGER)")
# Değişiklikleri kaydediyoruz
conn.commit()
# Tabloya bir kullanıcı ekliyoruz
# id = 1, money = 100
cur.execute("INSERT INTO users (id, money) VALUES (?, ?)", (1, 100))
# Değişiklikleri kaydediyoruz
conn.commit()
# Kullanıcının parasını sorguluyoruz
cur.execute("SELECT money FROM users WHERE id = ?", (1,))

# Sorgunun sonucunu alıyoruz
result = cur.fetchone()
# Sonucu ekrana yazdırıyoruz
print(result)
# Bağlantıyı kapatıyoruz
conn.close()