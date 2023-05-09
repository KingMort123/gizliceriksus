import discord
import sqlite3
from discord.ext import commands

# veritabanı dosyasına bağlanalım
conn = sqlite3.connect('money.db')
cursor = conn.cursor()

# sıralama komudunu içeren bir cog sınıfı tanımlayalım
class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ranking(self, ctx):
        # veritabanından kullanıcıların id ve money bilgilerini alalım
        cursor.execute("SELECT id, money FROM users ORDER BY money DESC")
        results = cursor.fetchall()

        # sonuçları bir liste haline getirelim
        ranking_list = []
        for i, result in enumerate(results):
            user_id = result[0]
            money = result[1]
            # kullanıcının discord adını alalım
            user = self.bot.get_user(user_id)
            if user is not None:
                user_name = user.name
            else:
                user_name = "Bilinmeyen"
            # listeye sıra numarası, kullanıcı adı ve money miktarını ekleyelim
            ranking_list.append(f"{i+1}. {user_name} - {money} coin")

        # listeyi bir mesaj haline getirelim
        ranking_message = "\n".join(ranking_list)

        # embed oluşturalım
        embed = discord.Embed(title="Para Sıralaması", color=discord.Color.green(), description="İşte para sıralaması:")
        # embed'e listeyi ekleyelim
        embed.add_field(name="Sıra", value=ranking_message)

        # embed'i gönderelim
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ranking(bot))