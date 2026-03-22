import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))
ANTI_RAID_LIMIT = int(os.getenv("ANTI_RAID_LIMIT", 5))
ANTI_RAID_TIME = int(os.getenv("ANTI_RAID_TIME", 10))