import requests
import time
import webbrowser
from update import send  # for Discord or custom updates

urls = [
    "https://secretsanta.cadbury.co.uk/code/a1008e92-b95d-4e13-a86e-fce60450ec7d",
    "https://secretsanta.cadbury.co.uk/code/76dd6a79-80db-40b2-957d-9658e7727d72",
    "https://secretsanta.cadbury.co.uk/code/4f8ed25b-2aeb-4986-9a30-08de1b353f4a",
    "https://secretsanta.cadbury.co.uk/code/2dd32a22-b8e6-40c6-e60d-08de1baaab95",
    "https://secretsanta.cadbury.co.uk/secretsanta/CfDJ8J-4L2JLEjBLsbt_V274SAuJTeQjpw-1Tzv8XqFJ3qdh5xkW817E3CQIpGYGq5zaygkRtuCU16Vdz3P4-pfzF-CM-aQJ-dtWQkFYPgOQlt2xS3jUxtwSiwS0rzG9ZJIAy5PAGWchU0r5",
    "https://secretsanta.cadbury.co.uk/code/e3759f5a-7b85-41ca-44c2-08de1c41764c",
    "https://secretsanta.cadbury.co.uk/code/311d9845-fce3-47ce-60f4-08de1c2c80de",
    "https://secretsanta.cadbury.co.uk/code/ec53918f-40d4-4794-d1a3-08dd1325334f",
    "https://secretsanta.cadbury.co.uk/code/c958f680-b052-4741-6546-08de1c2c80de",
    "https://secretsanta.cadbury.co.uk/code/e9157bb2-9890-4014-ac80-100d669ed362",
    "https://secretsanta.cadbury.co.uk/code/d1f53ad8-fa57-49fb-b7f0-fb110b8a812e",
    "https://secretsanta.cadbury.co.uk/secretsanta/CfDJ8J-4L2JLEjBLsbt_V274SAuz6j9GxI6MJ_SlwNHWwywFwDKpF0URDctiE9jnlfBSzWsTjAX7Uxqvg2ueEL4zmPI2JnJLKPLYSCHRe5JKCi5fusZ0me2pcm_bGHuZoJv3RZqakBvfWUSU?ar=False&codeId=CfDJ8J-4L2JLEjBLsbt_V274SAs5JMDu-XMsFN2RPxMMOAE9Kmnt7wDQ9s7hCPzvaKtPmnwtuulttWZMb0BhBZqriXME-wn0XpKXSDEhM2md50_JOEq-HwKnn9FTMJFYINsgeJxHYoD72B1O&utm_source=QR&utm_medium=QR_Code",
    "https://secretsanta.cadbury.co.uk/code/982cb88e-5764-462c-6f75-08de1d992242",
    "https://secretsanta.cadbury.co.uk/secretsanta/CfDJ8J-4L2JLEjBLsbt_V274SAthTLbuqJGombFSxRpxu2Jbty5idkvMITls-5-r-uwtJwWctvACr4U8b44sV1oCw8wYV0nBF4EBAr3g18GIcPobbXPOoSaqt9dZFDxerFpctcrgm0XOO-DJ",
    "https://secretsanta.cadbury.co.uk/code/63699f0c-b271-4055-85e2-08dcfdae2585",
    "https://secretsanta.cadbury.co.uk/code/631e209e-4a2b-4cc5-e280-08dcfdae24ce",
    "https://secretsanta.cadbury.co.uk/code/61d71f43-30ea-4685-8c1a-08dcfcd4f6a7",
    "https://secretsanta.cadbury.co.uk/code/7c019550-fa88-4260-94b0-ffaae170fbfd",
    "https://secretsanta.cadbury.co.uk/code/2693b6db-9274-4c66-b8ab-9f824d1afff5"
]

PLATFORMS = {
    "telegram": {
        "enabled": True,
        "token": "YOUR_BOT_TOKEN",
        "chat_id": "YOUR_CHAT_ID"
    },
    "twitter": {
        "enabled": True,
        "api_key": "YOUR_API_KEY",
        "api_secret": "YOUR_API_SECRET",
        "access_token": "YOUR_ACCESS_TOKEN",
        "access_secret": "YOUR_ACCESS_SECRET"
    },
    "facebook": {
        "enabled": True,
        "page_id": "YOUR_PAGE_ID",
        "access_token": "YOUR_ACCESS_TOKEN"
    },
    "reddit": {
        "enabled": True,
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "username": "YOUR_USERNAME",
        "password": "YOUR_PASSWORD",
        "subreddit": "freebies"
    }
}

def post_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{PLATFORMS['telegram']['token']}/sendMessage"
        data = {"chat_id": PLATFORMS['telegram']['chat_id'], "text": message, "parse_mode": "HTML"}
        requests.post(url, data=data)
        print("✅ Posted to Telegram")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

def post_to_twitter(message):
    try:
        import tweepy
        auth = tweepy.OAuthHandler(PLATFORMS['twitter']['api_key'], PLATFORMS['twitter']['api_secret'])
        auth.set_access_token(PLATFORMS['twitter']['access_token'], PLATFORMS['twitter']['access_secret'])
        api = tweepy.API(auth)
        api.update_status(message)
        print("✅ Posted to Twitter")
    except Exception as e:
        print(f"❌ Twitter error: {e}")

def post_to_facebook(message):
    try:
        url = f"https://graph.facebook.com/{PLATFORMS['facebook']['page_id']}/feed"
        params = {"message": message, "access_token": PLATFORMS['facebook']['access_token']}
        requests.post(url, params=params)
        print("✅ Posted to Facebook")
    except Exception as e:
        print(f"❌ Facebook error: {e}")

def post_to_reddit(message):
    try:
        import praw
        reddit = praw.Reddit(
            client_id=PLATFORMS['reddit']['client_id'],
            client_secret=PLATFORMS['reddit']['client_secret'],
            user_agent="SecretSantaBot/1.0",
            username=PLATFORMS['reddit']['username'],
            password=PLATFORMS['reddit']['password'],
        )
        subreddit = reddit.subreddit(PLATFORMS['reddit']['subreddit'])
        subreddit.submit(title="🎅 Cadbury Secret Santa Free Chocolate", selftext=message)
        print("✅ Posted to Reddit")
    except Exception as e:
        print(f"❌ Reddit error: {e}")

def share_everywhere(active_url):
    message = f"""
🎅 CADBURY SECRET SANTA - FREE CHOCOLATE! 🎁

✅ Active Link Found!

{active_url}

Get a FREE Cadbury chocolate bar sent to you or someone special!

Try it now before it runs out! 🍫

#FreeStuff #Cadbury #SecretSanta #FreeChocolate

Created by https://www.x.com/paparichens
"""
    if PLATFORMS['telegram']['enabled']:
        post_to_telegram(message)
    if PLATFORMS['twitter']['enabled']:
        post_to_twitter(message[:280])
    if PLATFORMS['facebook']['enabled']:
        post_to_facebook(message)
    if PLATFORMS['reddit']['enabled']:
        post_to_reddit(message)

def check_redirect(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        return response.url
    except requests.RequestException as e:
        return str(e)

def monitor_links(interval=60):
    print("🎅 Monitoring Cadbury Secret Santa links...")
    opened_urls = set()
    while True:
        for url in urls:
            final_url = check_redirect(url)
            if not final_url.startswith("http"):
                print(f"⚠️ Error checking {url}: {final_url}")
                continue
            if "missed-out" in final_url.lower():
                print(f"❌ Skipped (missed-out): {url}")
                continue
            if final_url not in opened_urls:
                print(f"✅ Found active link: {final_url}")
                opened_urls.add(final_url)
                share_everywhere(final_url)
                webbrowser.open(final_url)
                send(f"✅ Found active link: {final_url}")
        print("⏳ Waiting 60 seconds before next check...\n")
        time.sleep(interval)

if __name__ == "__main__":
    monitor_links()
