import discord
from discord.ext import commands
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

with open("config.json") as f:
    config = json.load(f)

WELCOME_CHANNEL = config["welcome_channel"]
TEMP_VC_CHANNEL = config["temp_vc_channel"]
TEMP_VC_CATEGORY = config["temp_vc_category"]

DEFAULT_LIMIT = config["vc_limit_default"]
MAX_LIMIT = config["vc_limit_max"]

BITRATE_LOW = config["bitrate_low"]
BITRATE_MEDIUM = config["bitrate_medium"]
BITRATE_HIGH = config["bitrate_high"]

COOLDOWN = config["vc_create_cooldown"]

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="?", intents=intents)

temp_vc = {}
cooldown = {}

vc_stats = {
    "created": 0,
    "active": 0,
    "peak_users": 0
}


# BOT READY
@bot.event
async def on_ready():
    print(f"Online: {bot.user}")


# WELCOME SYSTEM
@bot.event
async def on_member_join(member):

    if channel is None:
        return

    embed = discord.Embed(
        title="New Member!",
        description=f"{member.mention} Joined **{member.guild.name}**",
        color=discord.Color.green()
    )

    embed.add_field(
        name="> Member Count",
        value=f"> - ``{member.guild.member_count}``",
        inline=True
    )

    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text="Enjoy your stay!")

    await channel.send(embed=embed)

# Welcome Test Message
@bot.command()
async def testwelcome(ctx):

    member = ctx.author
    channel = bot.get_channel(WELCOME_CHANNEL)

    embed = discord.Embed(
        title="New Member!",
        description=f"{member.mention} Joined **{ctx.guild.name}**!",
        color=discord.Color.red()
    )

    embed.add_field(
        name="> Member Count",
        value=f"> - ``{ctx.guild.member_count}``",
        inline=True
    )

    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text="Test Welcome Message")

    await channel.send(embed=embed)

# AUTO BITRATE SYSTEM
async def optimize_bitrate(vc):

    users = len(vc.members)

    if users <= 2:
        bitrate = BITRATE_LOW
    elif users <= 5:
        bitrate = BITRATE_MEDIUM
    else:
        bitrate = BITRATE_HIGH

    try:
        await vc.edit(bitrate=bitrate)
    except:
        pass


# TEMP VC SYSTEM
@bot.event
async def on_voice_state_update(member, before, after):

    # create VC
    if after.channel and after.channel.id == TEMP_VC_CHANNEL:

        now = time.time()

        if member.id in cooldown:
            if now - cooldown[member.id] < COOLDOWN:
                await member.move_to(None)
                return

        cooldown[member.id] = now

        category = discord.utils.get(member.guild.categories, id=TEMP_VC_CATEGORY)

        vc = await member.guild.create_voice_channel(
            name=f"{member.name}'s Room",
            category=category,
            user_limit=DEFAULT_LIMIT
        )

        temp_vc[vc.id] = member.id

        vc_stats["created"] += 1
        vc_stats["active"] += 1

        await member.move_to(vc)

        await send_panel(vc, member)

    # delete VC
    if before.channel:

        if before.channel.id in temp_vc:

            if len(before.channel.members) == 0:

                vc_stats["active"] -= 1

                del temp_vc[before.channel.id]

                await before.channel.delete()

        else:
            await optimize_bitrate(before.channel)

    if after.channel:
        await optimize_bitrate(after.channel)


# DROPDOWN CONTROL PANEL
class VCPanel(discord.ui.View):

    def __init__(self, vc, owner):
        super().__init__(timeout=None)
        self.vc = vc
        self.owner = owner


    @discord.ui.select(
        placeholder="VC Controls",
        options=[
            discord.SelectOption(label="Transfer Owner", emoji="👑"),
            discord.SelectOption(label="Set User Limit", emoji="🎚"),
            discord.SelectOption(label="Kick Member", emoji="👢"),
            discord.SelectOption(label="Hide VC", emoji="👁"),
            discord.SelectOption(label="Unhide VC", emoji="👁‍🗨")
        ]
    )
    async def select_callback(self, interaction, select):

        if interaction.user.id != self.owner.id:
            await interaction.response.send_message(
                "Only VC owner can use this.", ephemeral=True
            )
            return

        choice = select.values[0]

        if choice == "Transfer Owner":

            members = [m for m in self.vc.members if m.id != self.owner.id]

            if not members:
                await interaction.response.send_message(
                    "No member available."
                )
                return

            new_owner = members[0]

            temp_vc[self.vc.id] = new_owner.id

            await interaction.response.send_message(
                f"👑 Owner transferred to {new_owner.mention}"
            )


        elif choice == "Set User Limit":

            new_limit = min(MAX_LIMIT, len(self.vc.members) + 2)

            await self.vc.edit(user_limit=new_limit)

            await interaction.response.send_message(
                f"🎚 Limit set to {new_limit}"
            )


        elif choice == "Kick Member":

            for m in self.vc.members:

                if m.id != self.owner.id:
                    await m.move_to(None)
                    await interaction.response.send_message(
                        f"👢 {m.name} kicked"
                    )
                    return

            await interaction.response.send_message("No member to kick.")


        elif choice == "Hide VC":

            await self.vc.set_permissions(
                interaction.guild.default_role,
                view_channel=False
            )

            await interaction.response.send_message("👁 VC Hidden")


        elif choice == "Unhide VC":

            await self.vc.set_permissions(
                interaction.guild.default_role,
                view_channel=True
            )

            await interaction.response.send_message("👁‍🗨 VC Visible")


# SEND PANEL
async def send_panel(vc, owner):

    embed = discord.Embed(
        title="🎛 VC Control Panel",
        description=f"Owner: {owner.mention}",
        color=discord.Color.blurple()
    )

    view = VCPanel(vc, owner)

    await vc.guild.system_channel.send(embed=embed, view=view)


# ADVANCED ANALYTICS
@bot.command()
async def vcanalytics(ctx):

    embed = discord.Embed(
        title="📊 Voice Channel Analytics",
        color=discord.Color.gold()
    )

    embed.add_field(
        name="VC Created",
        value=vc_stats["created"]
    )

    embed.add_field(
        name="Active VC",
        value=vc_stats["active"]
    )

    embed.add_field(
        name="Peak Users",
        value=vc_stats["peak_users"]
    )

    await ctx.send(embed=embed)


bot.run(TOKEN)
