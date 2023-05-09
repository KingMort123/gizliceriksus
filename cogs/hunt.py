prices = {
    "mouse": 10,
    "rabbit": 20,
    "deer": 40,
    "fox": 80,
    "lion_face": 160,
    "deagle": 50000,
    "dfrog": 75000,
    # buradan sonra eklediklerim
    "cat": 30, # yaygın bir evcil hayvan
    "dog": 40, # yaygın bir evcil hayvan
    "parrot": 60, # yaygın bir egzotik hayvan
    "horse": 100, # yaygın bir çiftlik hayvanı
    "elephant": 200, # nadir bir vahşi hayvan
    "panda": 300, # nadir bir vahşi hayvan
    "unicorn": 1000, # nadir bir efsanevi hayvan
    "dolphin": 500, # nadir bir deniz hayvanı
    "tiger": 800, # nadir ve tehlike altında bir vahşi hayvan
    "dragon": 5000, # nadir ve efsanevi bir hayvan
}

import discord
from discord.ext import commands
import random
import sqlite3

conn = sqlite3.connect("owo.db")
c = conn.cursor()


class hunt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("money.db")
        self.cursor = self.conn.cursor()

    @commands.command()
    async def hunt(self, ctx):
        # Kullanıcının ID'sini al
        user_id = ctx.author.id
        # Hayvanların isimlerini ve değerlerini listeler halinde al
        animals = list(prices.keys())
        values = list(prices.values())
        # Değerlere göre ağırlıklı bir seçim yap
        animal = random.choices(animals, k=1)[0]
        # Kullanıcıya hayvanı ver
        await ctx.send(f"{ctx.author.mention} {animal} yakaladı!")
        # Veritabanında zoo tablosuna hayvanı ekle veya güncelle
        c.execute("SELECT amount FROM zoo WHERE user_id = ? AND animal = ?", (user_id, animal))
        result = c.fetchone()
        if result:
            # Kullanıcının zaten bu hayvandan varsa miktarını arttır
            c.execute("UPDATE zoo SET amount = amount + 1 WHERE user_id = ? AND animal = ?", (user_id, animal))
            conn.commit()
        else:
            # Kullanıcının bu hayvandan yoksa yeni bir kayıt ekle
            c.execute("INSERT INTO zoo (user_id, animal, amount) VALUES (?, ?, ?)", (user_id, animal, 1))
            conn.commit()


    def update_money(self, user_id, amount):
    # Kullanıcının veritabanında olup olmadığını kontrol ediyoruz
     self.cursor.execute("SELECT money FROM users WHERE id = ?", (user_id,))
     result = self.cursor.fetchone()
     if result:
        # Kullanıcı varsa, parayı güncelliyoruz
        current_money = result[0]
        new_money = current_money + amount
        self.cursor.execute("UPDATE users SET money = ? WHERE id = ?", (new_money, user_id))
        self.conn.commit()
        return new_money
     else:
        # Kullanıcı yoksa, yeni bir kayıt oluşturuyoruz
        self.cursor.execute("INSERT INTO users (id, money) VALUES (?, ?)", (user_id, amount))
        self.conn.commit()
        return amount
    
    @commands.command()
    async def sell(self, ctx, animal: str, amount: int):
        # Kullanıcının ID'sini al
        user_id = ctx.author.id
        # Hayvanın değerini al
        value = prices[animal]
        # Kullanıcının hayvanlarını getir
        c.execute("SELECT amount FROM zoo WHERE user_id = ? AND animal = ?", (user_id, animal))
        result = c.fetchone()
        if result:
            # Kullanıcının bu hayvandan varsa
            current_amount = result[0]
            if amount <= current_amount:
                # Kullanıcı sattığı kadar hayvana sahipse
                # Hayvanların miktarını güncelle
                c.execute("UPDATE zoo SET amount = amount - ? WHERE user_id = ? AND animal = ?", (amount, user_id, animal))
                conn.commit()
                # Kullanıcının parasını güncelle
                new_money = self.update_money(user_id, value * amount)
                conn.commit()
                # Kullanıcıya mesaj gönder
                await ctx.send(f"{ctx.author.mention} {amount} tane {animal} sattı ve {value * amount} coins kazandı!")
            else:
                # Kullanıcı sattığı kadar hayvana sahip değilse
                await ctx.send(f"{ctx.author.mention} bahçende yeterli {animal} yok!")
        else:
            # Kullanıcının bu hayvandan yoksa
            await ctx.send(f"{ctx.author.mention} bahçende {animal} yok!")




    @commands.command()
    async def zoo(self, ctx, page: int = 1):
        # Kullanıcının ID'sini al
        user_id = ctx.author.id
        # Sayfa numarasını kontrol et
        if page < 1:
            page = 1
        # Sayfadaki hayvan sayısını belirle
        limit = 10
        # Sayfadaki ilk hayvanın indeksini hesapla
        offset = (page - 1) * limit
        # Kullanıcının hayvanlarını getir
        c.execute("SELECT animal, amount FROM zoo WHERE user_id = ? ORDER BY amount DESC LIMIT ? OFFSET ?", (user_id, limit, offset))
        result = c.fetchall()
        if result:
            # Kullanıcının hayvanları varsa bir mesaj oluştur
            message = f"{ctx.author.mention} bahçesindeki hayvanlar:\n"
            for row in result:
                animal, amount = row[0], row[1]
                message += f"{animal}: {amount}\n"
            # Mesajı gönder
            await ctx.send(message)
        else:
            # Kullanıcının hayvanı yoksa mesaj gönder
            await ctx.send(f"{ctx.author.mention} bahçende hiç hayvan yok!")
async def setup(bot):
    await bot.add_cog(hunt(bot))
