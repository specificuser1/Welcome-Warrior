import discord
from discord.ext import commands
from config import TOKEN, WELCOME_CHANNEL_ID

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="w", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# Welcome message when user joins
@bot.event
async def on_member_join(member):

    channel = bot.get_channel(WELCOME_CHANNEL_ID)

    if channel is None:
        return
    {member.mention}
    embed = discord.Embed(
        title="Welcome to the Server!",
        description=f"Welcome {member.mention} to **{member.guild.name}**!",
        color=discord.Color.green()
    )

    embed.add_field(
        name="> Member Count",
        value=f"''{member.guild.member_count}''",
        inline=True
    )

    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text="Enjoy your stay!")

    await channel.send(embed=embed)


# Test command
@bot.command()
async def arrior(ctx):

    member = ctx.author
    channel = bot.get_channel(WELCOME_CHANNEL_ID)

    embed = discord.Embed(
        title="Welcome to the Server!",
        description=f"Welcome {member.mention} to **{ctx.guild.name}**!",
        color=discord.Color.green()
    )

    embed.add_field(
        name="> Member Count",
        value=f"''{ctx.guild.member_count}''",
        inline=True
    )

    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text="Test Welcome Message")

    await channel.send(embed=embed)


bot.run(TOKEN)
