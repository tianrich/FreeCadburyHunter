import requests

webhook_url = "ENTER_DISCORD_WEBHOOK"

def send(content: str):
    data = {"content": content}
    try:
        resp = requests.post(webhook_url, json=data, timeout=10)
        if resp.status_code != 204:
            print(f"Discord webhook error: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Error sending to Discord: {e}")
