import discord
from discord.ext import commands
import sqlite3

# Database bağlantısını oluşturuyoruz
conn = sqlite3.connect("money.db")
# Database üzerinde işlem yapmak için bir cursor oluşturuyoruz
cursor = conn.cursor()
# Users tablosunu oluşturuyoruz (eğer yoksa)
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, money INTEGER)")
# Değişiklikleri kaydediyoruz
conn.commit()

# Cogs için bir sınıf oluşturuyoruz
class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Para ver komutunu tanımlıyoruz ve iki parametre alıyoruz: kullanıcı ve miktar
    @commands.command()
    async def give(self, ctx, user: discord.Member, amount: int):
        # Eğer miktar negatifse hata mesajı gönderiyoruz ve komutu sonlandırıyoruz
        if amount < 0:
            await ctx.send("Negatif bir miktar veremezsin.")
            return
        # Database'den komutu kullanan kişinin parasını alıyoruz (eğer yoksa 0 olarak varsayıyoruz)
        cursor.execute("SELECT money FROM users WHERE id = ?", (ctx.author.id,))
        sender_money = cursor.fetchone()
        if sender_money is None:
            sender_money = 0
        else:
            sender_money = sender_money[0]
        # Eğer komutu kullanan kişinin parası vermek istediği miktardan azsa hata mesajı gönderiyoruz ve komutu sonlandırıyoruz
        if sender_money < amount:
            await ctx.send("Yeterli paran yok. Daha az bir miktar ver.")
            return
        # Database'den para verilen kişinin parasını alıyoruz (eğer yoksa 0 olarak varsayıyoruz)
        cursor.execute("SELECT money FROM users WHERE id = ?", (user.id,))
        receiver_money = cursor.fetchone()
        if receiver_money is None:
            receiver_money = 0
        else:
            receiver_money = receiver_money[0]
        # Komutu kullanan kişinin parasından verilen miktarı çıkarıyoruz ve database'e kaydediyoruz
        sender_money -= amount
        cursor.execute("INSERT OR REPLACE INTO users (id, money) VALUES (?, ?)", (ctx.author.id, sender_money))
        conn.commit()
        # Para verilen kişinin parasına verilen miktarı ekliyoruz ve database'e kaydediyoruz
        receiver_money += amount
        cursor.execute("INSERT OR REPLACE INTO users (id, money) VALUES (?, ?)", (user.id, receiver_money))
        conn.commit()
        # Başarılı bir şekilde para verildiğini söylüyoruz
        await ctx.send(f"{ctx.author.mention}, {user.mention}'a {amount} para verdin.")
async def setup(bot):
    await bot.add_cog(Money(bot))
