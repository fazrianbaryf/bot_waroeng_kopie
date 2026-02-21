import discord
from discord.ext import commands, tasks
import os
import asyncio
import random
import database
from keep_alive import keep_alive
from datetime import datetime, timedelta, timezone

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

database.setup()

voice_tracker = {}
game_tracker = {}

KEYWORDS = ["mabar", "r", "login", "ready", "gas", "ayo", "main", "party", "rank", "push", "ayok", "skuy", "kuy", "mabar", "s", "v"]

# ===============================
# EVENT READY
# ===============================
@bot.event
async def on_ready():
    print(f"{bot.user} siap ngopi!")
    try:
        synced = await bot.tree.sync()
        print(f"Bisa nge-sync {len(synced)} slash command!")
    except Exception as e:
        print(e)
    check_voice.start()
    check_game.start()

# ===============================
# CHAT TRACKER
# ===============================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    content_words = content.split()
    
    # Cek apakah dia ngetag (mention) orang lain yang bukan bot dan bukan dirinya sendiri
    mentions_friend = any(not user.bot and user.id != message.author.id for user in message.mentions)
    
    # apakah ada kata kunci dalam pesan?
    contains_keyword = any(word in KEYWORDS for word in content_words)
    # apakah ada kata selain keyword (agar kita tidak spam jika hanya keyword saja)
    non_keyword_words = any(word not in KEYWORDS for word in content_words)
    
    if contains_keyword or mentions_friend:
        database.add_points(message.author.id, 2)
        await message.add_reaction("☕")
        await check_role(message.author)

    await bot.process_commands(message)

# ===============================
# VOICE TRACKER
# ===============================
@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel:
        voice_tracker[member.id] = datetime.now(timezone.utc)
    else:
        voice_tracker.pop(member.id, None)

@tasks.loop(minutes=10)
async def check_voice():
    await bot.wait_until_ready()
    if not bot.guilds:
        return
    now = datetime.now(timezone.utc)
    for user_id, join_time in list(voice_tracker.items()):
        if now - join_time >= timedelta(minutes=10):
            database.add_points(user_id, 5)
            voice_tracker[user_id] = now
            guild = bot.guilds[0]
            member = guild.get_member(user_id)
            if member:
                await check_role(member)

# ===============================
# GAME TRACKER
# ===============================
@tasks.loop(minutes=5)
async def check_game():
    await bot.wait_until_ready()
    if not bot.guilds:
        return
    guild = bot.guilds[0]
    for member in guild.members:
        if member.activity and isinstance(member.activity, discord.Game):
            database.add_points(member.id, 1)
            await check_role(member)

# ===============================
# ROLE SYSTEM
# ===============================
async def check_role(member):
    points = database.get_points(member.id)

    roles = {
        50: "Pelanggan Tetap",
        200: "Juragan Gorengan",
        500: "Sultan Kopi"
    }

    for point_req, role_name in roles.items():
        if points >= point_req:
            role = discord.utils.get(member.guild.roles, name=role_name)
            if role and role not in member.roles:
                await member.add_roles(role)

# ===============================
# COMMAND CEK
# ===============================
@bot.hybrid_command(name="cek", description="Cek saldo Biji Kopie lu yang kismin itu.")
async def cek(ctx: commands.Context):
    points = database.get_points(ctx.author.id)
    await ctx.send(f"🐒 Lu {ctx.author.mention} cuma punya **{points} Biji Kopie**, kismin amat anjir! 💩")

# ===============================
# COMMAND LEADERBOARD
# ===============================
@bot.hybrid_command(name="top_juragan", description="Liat daftar 10 Sengkuni penimbun Biji Kopie.")
async def top_juragan(ctx: commands.Context):
    await ctx.defer()
    leaderboard = database.get_leaderboard()
    text = "💀 **DAFTAR SENGKUNI SENGKUNI KITA** 💀\n"
    for i, (user_id, points) in enumerate(leaderboard, 1):
        user = bot.get_user(user_id) or await bot.fetch_user(user_id)
        text += f"{i}. {user.name} - {points} Biji Kopie doang 🤡\n"
    await ctx.send(text)

# ===============================
# COMMAND TRANSFER
# ===============================
@bot.hybrid_command(name="transfer", description="Sedekah Biji Kopie ke orang lain.")
async def transfer(ctx: commands.Context, member: discord.Member, amount: int):
    if amount <= 0:
        await ctx.send("🐒 Lu mau transfer angin bodoh? Masukin angka yang bener napa!")
        return
        
    sender_points = database.get_points(ctx.author.id)
    if sender_points < amount:
        await ctx.send(f"👽 Kaga ngotak njir! Saldo lu cuma {sender_points}, mau sok sedekah lu? 💩")
        return
        
    if member.bot:
        await ctx.send("🤖 Ngapain lu transfer ke bot bego? Ga waras lu!")
        return
        
    if member.id == ctx.author.id:
        await ctx.send("🤡 Sok sedekah ke diri sendiri! Gila hormat lu!")
        return

    # Kurangi poin pengirim
    database.add_points(ctx.author.id, -amount)
    # Tambah poin penerima
    database.add_points(member.id, amount)
    
    await ctx.send(f"💸 Cihuy! Si orang kaya {ctx.author.mention} abis sedekah **{amount} Biji Kopie** ke si gembel {member.mention}! 🐒")

# ===============================
# COMMAND SLOT (JUDI KOPI)
# ===============================
@bot.hybrid_command(name="slot", description="Judi Lingkaran Setan pakai Biji Kopie.")
async def slot(ctx: commands.Context, amount: int):
    if amount <= 0:
        await ctx.send("🤡 Modal lu kecil amat nyet! Taruhan harus lebih dari 0 dong!")
        return
        
    user_points = database.get_points(ctx.author.id)
    if user_points < amount:
        await ctx.send(f"💩 Biji Kopie lu cuma sisa {user_points}! Gausah sok main gede kalau kismin!")
        return
        
    # Kurangi poin taruhan di awal
    database.add_points(ctx.author.id, -amount)
        
    emojis = ["☕", "🐒", "👽", "🤡"]
    
    # Hasil akhir acak (Tentukan di awal)
    slot1, slot2, slot3 = random.choice(emojis), random.choice(emojis), random.choice(emojis)

    # Pesan awal animasi
    msg = await ctx.send(f"☠️ **JUDI LINGKARAN SETAN** ☠️\n{ctx.author.mention} nekat masang **{amount} Biji Kopie ☕**\n\n**[ 🔄 | 🔄 | 🔄 ]**\n\n*Bandar lagi ngocok duls...*")
    
    # Frame 1: Semua berputar
    await asyncio.sleep(0.6)
    await msg.edit(content=f"☠️ **JUDI LINGKARAN SETAN** ☠️\n{ctx.author.mention} nekat masang **{amount} Biji Kopie ☕**\n\n**[ {random.choice(emojis)} | {random.choice(emojis)} | {random.choice(emojis)} ]**\n\n*Ayo ayo bandar lagi milih...*")
    
    # Frame 2: Kunci slot 1
    await asyncio.sleep(0.6)
    await msg.edit(content=f"☠️ **JUDI LINGKARAN SETAN** ☠️\n{ctx.author.mention} nekat masang **{amount} Biji Kopie ☕**\n\n**[ {slot1} | {random.choice(emojis)} | {random.choice(emojis)} ]**\n\n*Tahan napas lu anjing...*")
    
    # Frame 3: Kunci slot 1 & 2
    await asyncio.sleep(0.6)
    await msg.edit(content=f"☠️ **JUDI LINGKARAN SETAN** ☠️\n{ctx.author.mention} nekat masang **{amount} Biji Kopie ☕**\n\n**[ {slot1} | {slot2} | {random.choice(emojis)} ]**\n\n*Satu lagi cok deg degan ga lu...*")
    
    await asyncio.sleep(0.8)
    
    result_text = f"☠️ **HASIL JUDI LINGKARAN SETAN** ☠️\n"
    result_text += f"{ctx.author.mention} korban masang **{amount} Biji Kopie ☕**\n\n"
    result_text += f"**[ {slot1} | {slot2} | {slot3} ]**\n\n"
    
    # Menang jackpot
    if slot1 == slot2 == slot3:
        winnings = amount * 5
        database.add_points(ctx.author.id, winnings)
        result_text += f"🔥 **JACKPOT GILA!** Lu hokinya ga ngotak! Dapet **{winnings} Biji Kopie**, bandar bangkrut asu! 🔥"
    # Menang biasa
    elif slot1 == slot2 or slot2 == slot3 or slot1 == slot3:
        winnings = amount * 2
        database.add_points(ctx.author.id, winnings)
        result_text += f"🐒 **LUMAYAN BALIK MODAL!** Lu dapet **{winnings} Biji Kopie**, sujud syukur kek! 👽"
    # Kalah bandar
    else:
        result_text += f"💀 **MAMPUS RUNGKAD!** Lu ilang {amount} Biji Kopie anjir. Dah gw bilang gausah main judi gila! 🤡"
        
    await msg.edit(content=result_text)

# ===============================
# START
# ===============================
keep_alive()
bot.run(TOKEN)