from pprint import pprint
import requests

bot_token = "847588157:AAEZoJzdNwKzPsxaKGOKhDqV9XYqoQtZYBU"
base_url = "https://aaa3f830.ngrok.io"
test_url = f"{base_url}/{bot_token}"

def get_url(method):
    return f"https://api.telegram.org/bot{bot_token}/{method}"

r = requests.get(get_url("setWebhook"), data={"url": test_url})
r = requests.get(get_url("getWebhookInfo"))
pprint(r.status_code)
pprint(r.json())