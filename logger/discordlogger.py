from discord_webhook import DiscordWebhook

from logger.logger import Logger


class DiscordLogger(Logger):

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def log(self, line: str) -> None:
        webhook = DiscordWebhook(url=self.webhook_url, content=line)
        webhook.execute()
