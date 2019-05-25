import requests
from .configs import settings


class DiscordBot:
    def __init__(self, webhook):
        self.webhook = webhook

    def send_message(self, message):
        msg = "**{}**: {}".format(settings.SERVER, message)
        requests.post(self.webhook, json={"content": msg})

    def big_sale_notify(self, pid, sale):
        message = "**{}**: [Too Big Sale] product id **{}** have sale **{}**".format(settings.SERVER, pid, sale)
        self.send_message(message)


discord = DiscordBot(settings.WEBHOOK_URL)