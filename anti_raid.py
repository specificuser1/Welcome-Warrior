import time
from collections import deque
from config import ANTI_RAID_LIMIT, ANTI_RAID_TIME

class AntiRaid:

    def __init__(self):
        self.joins = deque()

    def check(self):

        now = time.time()
        self.joins.append(now)

        while self.joins and now - self.joins[0] > ANTI_RAID_TIME:
            self.joins.popleft()

        if len(self.joins) >= ANTI_RAID_LIMIT:
            return True

        return False


antiraid = AntiRaid()