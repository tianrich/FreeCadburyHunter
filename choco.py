import requests
import time
import webbrowser
from update import send
 
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
    "https://secretsanta.cadbury.co.uk/code/982cb88e-5764-462c-6f75-08de1d992242"
]

def check_redirect(url): 
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        return response.url
    except requests.RequestException as e:
        return str(e)

def monitor_links(interval=60):
    print("🎅 Monitoring Cadbury Secret Santa links...")
    while True:
        for url in urls:
            final_url = check_redirect(url)

            # If request failed, skip
            if not final_url.startswith("http"):
                print(f"⚠️ Error checking {url}: {final_url}")
                continue

            # Skip links that end up at 'missed-out'
            if "missed-out" in final_url.lower():
                print(f"❌ Skipped (missed-out): {url}")
                continue

            # Otherwise open the working one
            print(f"✅ Found active link: {final_url}")
            #send(f"✅ Found active link: {final_url}")
            webbrowser.open(final_url)

        # Wait before next check
        print("⏳ Waiting 60 seconds before next check...\n")
        time.sleep(interval)

if __name__ == "__main__":
    monitor_links()
