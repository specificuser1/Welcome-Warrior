import discord
from discord.ext import commands
from config import TOKEN, WELCOME_CHANNEL_ID
from welcome_card import generate_card
from stats import stats
from anti_raid import antiraid

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")


@bot.event
async def on_member_join(member):

    if antiraid.check():
        print("⚠ RAID DETECTED")
        return

    stats.add_join()

    channel = bot.get_channel(WELCOME_CHANNEL_ID)

    avatar = member.avatar.url if member.avatar else member.default_avatar.url

    img = generate_card(member.name, avatar, member.guild.member_count)

    file = discord.File(img)

    await channel.send(
        content=f"Welcome {member.mention}",
        file=file
    )


@bot.command()
async def testwelcome(ctx):

    member = ctx.author

    avatar = member.avatar.url if member.avatar else member.default_avatar.url

    img = generate_card(member.name, avatar, ctx.guild.member_count)

    file = discord.File(img)

    await ctx.send(file=file)


@bot.command()
async def joinstats(ctx):

    data = stats.get_stats()

    embed = discord.Embed(
        title="Join Statistics",
        color=discord.Color.blue()
    )

    embed.add_field(name="Total Joins", value=data["total"])
    embed.add_field(name="Today", value=data["today"])

    await ctx.send(embed=embed)


bot.run(TOKEN)