import discord
from discord.ext import commands
import asyncio
import sqlite3

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Cog dosyalarını bulmak için os modülünü kullanıyoruz
import os

async def load_extensions():
   for f in os.listdir("./cogs"):
	   if f.endswith(".py"):
		   await bot.load_extension("cogs." + f[:-3])

# Cog dosyalarının sonunda .py olduğunu varsayıyoruz
asyncio.run(load_extensions())

# Veritabanı bağlantısını tanımlıyoruz
conn = sqlite3.connect("money.db")
cur = conn.cursor()

# Para gösterme komutu için bir fonksiyon yazıyoruz
@bot.command()
async def para(ctx):
    # Kullanıcının ID'sini alıyoruz
    user_id = ctx.author.id
    # Kullanıcının parasını veritabanından sorguluyoruz
    cur.execute("SELECT money FROM users WHERE id = ?", (user_id,))
    user_money = cur.fetchone()
    if user_money:
        user_money = user_money[0]
    else:
        # Kullanıcı veritabanında yoksa, başlangıç parası olarak 100 TL veriyoruz
        user_money = 100
        cur.execute("SELECT money FROM users WHERE id = ?", (user_id,))
        conn.commit()
    # Bir embed nesnesi oluşturuyoruz
    embed = discord.Embed(title=f"{ctx.author.name} adlı kullanıcının parası", description=f"{user_money} TL", color=discord.Color.green())
    # Embed nesnesine bir resim ekliyoruz
    # Resmi yerel olarak kullanmak için discord.File() fonksiyonunu kullanıyoruz
    file = discord.File("money.png", filename="money.png")
    embed.set_image(url="attachment://money.png")
    # Embed nesnesini gönderiyoruz
    await ctx.send(file=file, embed=embed)

bot.run("NzUyMTQ4MDE3ODI1NDQ3OTc3.GjkpWW.t3sl_V8cHF-0xzrKAnnhxqDtVrsoRROtfYDYa0")