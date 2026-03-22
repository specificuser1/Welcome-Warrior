class JoinStats:

    def __init__(self):
        self.total_joins = 0
        self.today_joins = 0

    def add_join(self):
        self.total_joins += 1
        self.today_joins += 1

    def get_stats(self):
        return {
            "total": self.total_joins,
            "today": self.today_joins
        }


stats = JoinStats()