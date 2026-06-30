class DatabaseMixIn:
    """Injects standardized database connection streams into framework classes."""
    def __init__(self, bot, connection, queries):
        self.bot = bot
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.queries = queries