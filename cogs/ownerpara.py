import discord
from discord.ext import commands
import sqlite3

# SQLite database bağlantısı ve cursor oluştur
conn = sqlite3.connect("money.db")
cur = conn.cursor()

# Cog sınıfı tanımla
class ownerpara(commands.Cog):
    # Cog'un başlatıcı fonksiyonu
    def __init__(self, bot):
        self.bot = bot

    # send_money komutu
    @commands.command()
    @commands.is_owner() # Sadece botun sahibi kullanabilir
    async def send_money(self, ctx, member: discord.Member, amount: int):
        # İstediğiniz kişiye ve istediğiniz miktarda para gönderir
        # Para databaseden çekilir ve değiştirilir
        cur.execute("SELECT money FROM users WHERE id = ?", (member.id,))
        row = cur.fetchone()
        if row:
            new_money = row[0] + amount
            cur.execute("UPDATE users SET money = ? WHERE id = ?", (new_money, member.id))
        else:
            cur.execute("INSERT INTO users (id, money) VALUES (?, ?)", (member.id, amount))
        conn.commit()
        await ctx.send(f"{ctx.author.mention} {member.mention}'a {amount} TL gönderdi.")

# Cog'u yükleme fonksiyonu
async def setup(bot):
    await bot.add_cog(ownerpara(bot))