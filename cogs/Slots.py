import discord
from discord.ext import commands
import random
import sqlite3
import asyncio

# Database bağlantısını oluşturuyoruz
conn = sqlite3.connect("money.db")
# Database üzerinde işlem yapmak için bir cursor oluşturuyoruz
cursor = conn.cursor()
# Users tablosunu oluşturuyoruz (eğer yoksa)
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, money INTEGER)")
# Değişiklikleri kaydediyoruz
conn.commit()

# Cogs için bir sınıf oluşturuyoruz
class Slot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Owo slot komutunu tanımlıyoruz ve bir parametre alıyoruz
    @commands.command()
    async def slot(self, ctx, amount: int):
           # Database'den kullanıcının parasını alıyoruz (eğer yoksa 0 olarak varsayıyoruz)
        cursor.execute("SELECT money FROM users WHERE id = ?", (ctx.author.id,))
        money = cursor.fetchone()
        if money is None:
            money = 0
        else:
            money = money[0]
        # Eğer kullanıcının parası oynadığı miktardan azsa oynayamayacağını söylüyoruz ve komutu sonlandırıyoruz
        if money < amount:
            await ctx.send("Yeterli paran yok. Daha az bir miktarla oynamayı dene.")
            return       
        # Slot makinesindeki sembolleri bir liste olarak tanımlıyoruz
        symbols = ["💎", "🀄", "⭐", "<:head:1074642340158914570>", "<:emoji_21:1090555441878151231>","<:w_:1090555393983402016>", "<a:coinflip:1074661933820690512>"]
        
         # Üç tane rastgele sembol seçiyoruz
        owoemojio="<:emoji_21:1090555441878151231>"
        owoemojiw ="<:w_:1090555393983402016>"
        slot1 = "<a:slot:1090552312361144411>"
        slot2 = "<a:slot:1090552312361144411>"
        slot3 = "<a:slot:1090552312361144411>"
        # Slot makinesinin ilk halini bir embed olarak oluşturuyoruz
        embed = discord.Embed(title="Slot", description=f"{slot1} | {slot2} | {slot3}", color=discord.Color.random())
        # Embed'i bir mesaj olarak gönderiyoruz
        message = await ctx.send(embed=embed)
        # Bir saniye bekliyoruz
        await asyncio.sleep(1)
        # Slot makinesinin ikinci halini embed'i güncelleyerek gösteriyoruz
        slot1 = random.choice(symbols)
        embed.description = f"{slot1} | {slot2} | {slot3}"
        await message.edit(embed=embed)
        # Bir saniye daha bekliyoruz
        await asyncio.sleep(1)
        # Slot makinesinin son halini embed'i güncelleyerek gösteriyoruz
        slot3 = random.choice(symbols)
        embed.description = f"{slot1} | {slot2} | {slot3}"
        await message.edit(embed=embed)
        await asyncio.sleep(1)
        # Slot makinesinin ikinci halini embed'i güncelleyerek gösteriyoruz
        slot2 = random.choice(symbols)
        embed.description = f"{slot1} | {slot2} | {slot3}"
        await message.edit(embed=embed)
        # Eğer üç sembol de aynıysa kazandınız mesajı gönderiyoruz ve database'den para ekliyoruz
        if slot1 == slot2 == slot3:
            # Embed'i yeşil renge boyuyoruz ve kazandınız mesajını ekliyoruz
            embed.color = discord.Color.green()
            embed.add_field(name="Tebrikler! Kazandınız!", value="Tebrikler.")
            # Embed'i güncelliyoruz
            await message.edit(embed=embed)
            # Database'den kullanıcının parasını alıyoruz (eğer yoksa 0 olarak varsayıyoruz)
            cursor.execute("SELECT money FROM users WHERE id = ?", (ctx.author.id,))
            money = cursor.fetchone()
            if money is None:
                money = 0
            else:
                money = money[0]

            # Kullanıcının parasına oynadığı miktarın belirli bir katını ekliyoruz ve database'e kaydediyoruz
            # Eğer sembol 💎 ise 10 katı, eğer 🀄 ise 3 katı, eğer 👤 ise 4 katı, eğer ⭐ ise aynı miktar, eğer başka bir sembol ise 2 katı ekliyoruz
            if slot1==slot2==slot3 == "💎":
                multiplier = 20
            elif slot1==slot2==slot3 == "🀄":
                multiplier = 5
            elif slot1==slot2==slot3 == "<:head:1074642340158914570>":
                multiplier = 4
            elif slot1==slot2==slot3 == "⭐":
                multiplier = 1
            elif slot1==slot2==slot3 == "<a:coinflip:1074661933820690512>":
                multiplier = 30
            else:
                multiplier = 1
            money += amount * multiplier
            cursor.execute("INSERT OR REPLACE INTO users (id, money) VALUES (?, ?)", (ctx.author.id, money))
            conn.commit()
           
        # Eğer değilse kaybettiniz mesajı gönderiyoruz ve database'den para çıkarıyoruz
        else:
            # Embed'i kırmızı renge boyuyoruz ve kaybettiniz mesajını ekliyoruz
            embed.color = discord.Color.red()
            embed.add_field(name="Üzgünüm, kaybettiniz.", value="Tekrar Deneyin")
            # Embed'i güncelliyoruz
            await message.edit(embed=embed)
            # Database'den kullanıcının parasını alıyoruz (eğer yoksa 0 olarak varsayıyoruz)
            cursor.execute("SELECT money FROM users WHERE id = ?", (ctx.author.id,))
            money = cursor.fetchone()
            if money is None:
                money = 0
            else:
                money = money[0]
            # Kullanıcının parasından oynadığı miktarı çıkarıyoruz ve database'e kaydediyoruz (eğer para negatif olursa 0 olarak ayarlıyoruz)
            money -= amount
            if money < 0:
                money = 0
            cursor.execute("INSERT OR REPLACE INTO users (id, money) VALUES (?, ?)", (ctx.author.id, money))
            conn.commit()
async def setup(bot):
    await bot.add_cog(Slot(bot))