import discord
from discord.ext import commands
import random
import sqlite3

# SQLite database bağlantısı ve cursor oluştur
conn = sqlite3.connect("money.db")
cur = conn.cursor()

# users tablosunu oluştur veya varsa geç
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, money INTEGER)")

# Kullanıcının parasını database'den okuyan fonksiyon
def get_money(user: discord.User):
    cur.execute("SELECT money FROM users WHERE id = ?", (user.id,))
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        return 0

# Kullanıcının parasını database'de değiştiren fonksiyon
def change_money(user: discord.User, amount: int):
    cur.execute("SELECT money FROM users WHERE id = ?", (user.id,))
    row = cur.fetchone()
    if row:
        new_money = row[0] + amount
        cur.execute("UPDATE users SET money = ? WHERE id = ?", (new_money, user.id))
    else:
        cur.execute("INSERT INTO users (id, money) VALUES (?, ?)", (user.id, amount))
    conn.commit()

# Cog sınıfı tanımla
class Fun(commands.Cog):
    # Cog'un başlatıcı fonksiyonu
    def __init__(self, bot):
        self.bot = bot

    # Coinflip komutu
    @commands.command()
    async def coinflip(self, ctx, guess: str, bet: str):
        # Tahminin yazı veya tura olup olmadığını kontrol et
        if guess.lower() not in ["yazı", "tura"]:
            await ctx.send("Lütfen yazı veya tura olarak tahminde bulunun.")
            return
        # Bahsin pozitif olup olmadığını veya all olup olmadığını kontrol et
        if bet.lower() == "all":
            bet = 350000 # All deyince 350k oynar
        else:
            try:
                bet = int(bet) # Bahsi tam sayıya dönüştür
                if bet <= 0:
                    await ctx.send("Lütfen pozitif bir sayı girin.")
                    return
            except ValueError:
                await ctx.send("Lütfen geçerli bir sayı girin.")
                return
        # Kullanıcının yeterli parası olup olmadığını kontrol et
        money = get_money(ctx.author)
        if money < bet:
            await ctx.send("Yeterli paranız yok.")
            return
        # Para dönüyor... mesajı gönder
        await ctx.send(f"{ctx.author.mention} para dönüyor...")
        # Rastgele yazı veya tura seç
        result = random.choice(["yazı", "tura"])
        # Sonucu gösteren embed oluştur
        embed = discord.Embed(title="Coinflip", description=f"Para {result} geldi!")
        # Sonuca göre kullanıcıyı etiketle ve parayı değiştir
        if guess.lower() == result:
            embed.add_field(name="Sonuç", value=f"{ctx.author.mention} kazandın! {bet} TL aldın.")
            change_money(ctx.author, bet)
        else:
            embed.add_field(name="Sonuç", value=f"{ctx.author.mention} kaybettin! {bet} TL kaybettin.")
            change_money(ctx.author, -bet)
        # Embed'i gönder
        await ctx.send(embed=embed)

# Cog'u yükleme fonksiyonu
async def setup(bot):
    await bot.add_cog(Fun(bot))