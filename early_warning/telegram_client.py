import requests

class TelegramClient:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'

    def send_warning(self, caption, image_path):
        files = {'photo': open(image_path, 'rb')}
        data = {'chat_id': self.chat_id, 'caption': caption}
        resp = requests.post(self.api_url, data=data, files=files)
        resp.raise_for_status()

