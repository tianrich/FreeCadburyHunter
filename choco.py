import asyncio
import random
import signal
import sys
import webbrowser
import os
from typing import Set, Dict, Optional
from urllib.parse import urlparse, quote
from datetime import datetime
import json

from playwright.async_api import async_playwright

# ============================================================================
# SOCIAL MEDIA API CONFIGURATION
# ============================================================================
# Set these as environment variables or edit directly for API automation
SOCIAL_CONFIG = {
    "twitter": {
        "enabled": os.getenv("TWITTER_ENABLED", "true").lower() == "true",
        "api_key": os.getenv("TWITTER_API_KEY", ""),
        "api_secret": os.getenv("TWITTER_API_SECRET", ""),
        "access_token": os.getenv("TWITTER_ACCESS_TOKEN", ""),
        "access_secret": os.getenv("TWITTER_ACCESS_SECRET", ""),
        "bearer_token": os.getenv("TWITTER_BEARER_TOKEN", ""),
    },
    "facebook": {
        "enabled": os.getenv("FACEBOOK_ENABLED", "true").lower() == "true",
        "access_token": os.getenv("FACEBOOK_ACCESS_TOKEN", ""),
        "page_id": os.getenv("FACEBOOK_PAGE_ID", ""),
    },
    "instagram": {
        "enabled": os.getenv("INSTAGRAM_ENABLED", "false").lower() == "true",
        "access_token": os.getenv("INSTAGRAM_ACCESS_TOKEN", ""),
        "business_account_id": os.getenv("INSTAGRAM_BUSINESS_ID", ""),
    },
    "linkedin": {
        "enabled": os.getenv("LINKEDIN_ENABLED", "false").lower() == "true",
        "access_token": os.getenv("LINKEDIN_ACCESS_TOKEN", ""),
        "person_id": os.getenv("LINKEDIN_PERSON_ID", ""),
    },
    "reddit": {
        "enabled": os.getenv("REDDIT_ENABLED", "false").lower() == "true",
        "client_id": os.getenv("REDDIT_CLIENT_ID", ""),
        "client_secret": os.getenv("REDDIT_CLIENT_SECRET", ""),
        "username": os.getenv("REDDIT_USERNAME", ""),
        "password": os.getenv("REDDIT_PASSWORD", ""),
        "subreddit": os.getenv("REDDIT_SUBREDDIT", "freebies"),
    },
    "telegram": {
        "enabled": os.getenv("TELEGRAM_ENABLED", "false").lower() == "true",
        "bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
        "chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
    },
    "discord": {
        "enabled": os.getenv("DISCORD_ENABLED", "false").lower() == "true",
        "webhook_url": os.getenv("DISCORD_WEBHOOK_URL", ""),
    },
    "slack": {
        "enabled": os.getenv("SLACK_ENABLED", "false").lower() == "true",
        "webhook_url": os.getenv("SLACK_WEBHOOK_URL", ""),
    },
    "whatsapp": {
        "enabled": os.getenv("WHATSAPP_ENABLED", "false").lower() == "true",
        "business_id": os.getenv("WHATSAPP_BUSINESS_ID", ""),
        "access_token": os.getenv("WHATSAPP_ACCESS_TOKEN", ""),
        "phone_number_id": os.getenv("WHATSAPP_PHONE_NUMBER_ID", ""),
    },
    "mastodon": {
        "enabled": os.getenv("MASTODON_ENABLED", "false").lower() == "true",
        "instance_url": os.getenv("MASTODON_INSTANCE", "https://mastodon.social"),
        "access_token": os.getenv("MASTODON_ACCESS_TOKEN", ""),
    },
    "bluesky": {
        "enabled": os.getenv("BLUESKY_ENABLED", "false").lower() == "true",
        "handle": os.getenv("BLUESKY_HANDLE", ""),
        "app_password": os.getenv("BLUESKY_APP_PASSWORD", ""),
    },
    "threads": {
        "enabled": os.getenv("THREADS_ENABLED", "false").lower() == "true",
        "access_token": os.getenv("THREADS_ACCESS_TOKEN", ""),
        "user_id": os.getenv("THREADS_USER_ID", ""),
    },
}

# Credit configuration
CREDIT_HANDLE = "@paparichens"
CREDIT_URL = "https://www.x.com/paparichens"

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
    "https://secretsanta.cadbury.co.uk/code/2693b6db-9274-4c66-b8ab-9f824d1afff5",
]

opened_destinations: Set[str] = set()
BAD_URL_CONTAINS = "missed-out"

# ============================================================================
# MESSAGE TEMPLATES
# ============================================================================

def get_share_message(url: str, platform: str = "default") -> str:
    """Generate platform-specific share messages with credit"""
    timestamp = datetime.now().strftime("%H:%M")
    
    templates = {
        "twitter": f"🎅🎁 LIVE Cadbury Secret Santa Link!\n\n✅ Active now at {timestamp}\n{url}\n\n🍫 Grab your free chocolate!\n\nCredit: {CREDIT_HANDLE}\n#CadburySecretSanta #Freebie #FreeChocolate",
        
        "facebook": f"🎅🎁 Cadbury Secret Santa - ACTIVE LINK!\n\nJust found an active link at {timestamp}! Get your free Cadbury chocolate here:\n\n{url}\n\n🍫 Click fast before it expires!\n\nThanks to {CREDIT_HANDLE} for the heads up!\n\n#CadburySecretSanta #FreeChocolate #Freebies",
        
        "linkedin": f"🎅 Cadbury Secret Santa Alert\n\nActive promotional link detected at {timestamp}. Complimentary Cadbury product available:\n\n{url}\n\nCredit: {CREDIT_HANDLE}\n\n#Marketing #Promotion #Cadbury",
        
        "reddit": f"🎅🎁 [LIVE NOW] Cadbury Secret Santa Active Link - Free Chocolate!\n\nJust verified active at {timestamp}:\n{url}\n\n🍫 Grab it while it lasts!\n\nCredit to {CREDIT_HANDLE} on X/Twitter",
        
        "telegram": f"🎅🎁 *CADBURY SECRET SANTA - LIVE!*\n\n✅ Active link found at {timestamp}\n\n🔗 {url}\n\n🍫 Click now for free Cadbury chocolate!\n\n_Credit: {CREDIT_HANDLE}_",
        
        "discord": f"🎅🎁 **CADBURY SECRET SANTA - ACTIVE LINK!**\n\n✅ Live at {timestamp}\n\n{url}\n\n🍫 Free chocolate - hurry!\n\nCredit: {CREDIT_HANDLE}",
        
        "slack": f"🎅🎁 *Cadbury Secret Santa - Active Link!*\n\nFound at {timestamp}\n{url}\n\n🍫 Free Cadbury chocolate available now!\n\nCredit: {CREDIT_HANDLE}",
        
        "whatsapp": f"🎅🎁 Cadbury Secret Santa LIVE!\n\n✅ Active at {timestamp}\n{url}\n\n🍫 Free chocolate - click now!\n\nCredit: {CREDIT_HANDLE}",
        
        "mastodon": f"🎅🎁 Cadbury Secret Santa - Active Link Found!\n\n✅ Live at {timestamp}\n{url}\n\n🍫 Free Cadbury chocolate available!\n\nCredit: {CREDIT_HANDLE}\n\n#CadburySecretSanta #Freebie #FreeChocolate",
        
        "bluesky": f"🎅🎁 LIVE Cadbury Secret Santa!\n\n✅ Active at {timestamp}\n{url}\n\n🍫 Free chocolate!\n\nCredit: {CREDIT_HANDLE}",
        
        "threads": f"🎅🎁 Cadbury Secret Santa - ACTIVE NOW!\n\n✅ Found at {timestamp}\n{url}\n\n🍫 Get your free Cadbury chocolate!\n\nCredit: {CREDIT_HANDLE}",
        
        "instagram": f"🎅🎁 Cadbury Secret Santa LIVE!\n\nActive link in bio! Free Cadbury chocolate available now at {timestamp} 🍫\n\nCredit: {CREDIT_HANDLE}\n\n#CadburySecretSanta #FreeChocolate #Freebie #Cadbury",
    }
    
    return templates.get(platform, templates["twitter"])

# ============================================================================
# SOCIAL MEDIA POSTING FUNCTIONS
# ============================================================================

async def post_to_twitter(url: str, session) -> bool:
    """Post to Twitter/X using API v2"""
    if not SOCIAL_CONFIG["twitter"]["enabled"]:
        return False
    
    try:
        import aiohttp
        
        bearer_token = SOCIAL_CONFIG["twitter"]["bearer_token"]
        if not bearer_token:
            print("  ⚠️ Twitter: No bearer token configured")
            return False
        
        message = get_share_message(url, "twitter")
        
        api_url = "https://api.twitter.com/2/tweets"
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        }
        payload = {"text": message}
        
        async with session.post(api_url, json=payload, headers=headers) as resp:
            if resp.status == 201:
                print(f"  ✅ Posted to Twitter/X!")
                return True
            else:
                print(f"  ❌ Twitter error: {resp.status} - {await resp.text()}")
                return False
                
    except Exception as e:
        print(f"  ❌ Twitter error: {e}")
        return False

async def post_to_facebook(url: str, session) -> bool:
    """Post to Facebook Page"""
    if not SOCIAL_CONFIG["facebook"]["enabled"]:
        return False
    
    try:
        import aiohttp
        
        access_token = SOCIAL_CONFIG["facebook"]["access_token"]
        page_id = SOCIAL_CONFIG["facebook"]["page_id"]
        
        if not access_token or not page_id:
            print("  ⚠️ Facebook: Missing credentials")
            return False
        
        message = get_share_message(url, "facebook")
        
        api_url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
        payload = {
            "message": message,
            "link": url,
            "access_token": access_token,
        }
        
        async with session.post(api_url, data=payload) as resp:
            if resp.status == 200:
                print(f"  ✅ Posted to Facebook!")
                return True
            else:
                print(f"  ❌ Facebook error: {resp.status}")
                return False
                
    except Exception as e:
        print(f"  ❌ Facebook error: {e}")
        return False

async def post_to_linkedin(url: str, session) -> bool:
    """Post to LinkedIn"""
    if not SOCIAL_CONFIG["linkedin"]["enabled"]:
        return False
    
    try:
        import aiohttp
        
        access_token = SOCIAL_CONFIG["linkedin"]["access_token"]
        person_id = SOCIAL_CONFIG["linkedin"]["person_id"]
        
        if not access_token or not person_id:
            print("  ⚠️ LinkedIn: Missing credentials")
            return False
        
        message = get_share_message(url, "linkedin")
        
        api_url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }
        payload = {
            "author": f"urn:li:person:{person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": message},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }
        
        async with session.post(api_url, json=payload, headers=headers) as resp:
            if resp.status == 201:
                print(f"  ✅ Posted to LinkedIn!")
                return True
            else:
                print(f"  ❌ LinkedIn error: {resp.status}")
                return False
                
    except Exception as e:
        print(f"  ❌ LinkedIn error: {e}")
        return False

async def post_to_reddit(url: str, session) -> bool:
    """Post to Reddit"""
    if not SOCIAL_CONFIG["reddit"]["enabled"]:
        return False
    
    try:
        import aiohttp
        
        config = SOCIAL_CONFIG["reddit"]
        if not all([config["client_id"], config["client_secret"], config["username"], config["password"]]):
            print("  ⚠️ Reddit: Missing credentials")
            return False
        
        # Get access token
        auth = aiohttp.BasicAuth(config["client_id"], config["client_secret"])
        token_data = {
            "grant_type": "password",
            "username": config["username"],
            "password": config["password"],
        }
        
        async with session.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data=token_data,
            headers={"User-Agent": "CadburyMonitor/1.0"},
        ) as resp:
            token_response = await resp.json()
            access_token = token_response.get("access_token")
        
        if not access_token:
            print("  ❌ Reddit: Failed to get access token")
            return False
        
        # Post to subreddit
        title = f"🎅🎁 [LIVE] Cadbury Secret Santa - Free Chocolate Available Now!"
        message = get_share_message(url, "reddit")
        
        post_data = {
            "sr": config["subreddit"],
            "kind": "self",
            "title": title,
            "text": message,
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "CadburyMonitor/1.0",
        }
        
        async with session.post(
            "https://oauth.reddit.com/api/submit",
            data=post_data,
            headers=headers,
        ) as resp:
            if resp.status == 200:
                print(f"  ✅ Posted to Reddit (r/{config['subreddit']})!")
                return True
            else:
                print(f"  ❌ Reddit error: {resp.status}")
                return False
                
    except Exception as e:
        print(f"  ❌ Reddit error: {e}")
        return False

async def post_to_telegram(url: str, session) -> bool:
    """Post to Telegram"""
    if not SOCIAL_CONFIG["telegram"]["enabled"]:
        return False
    
    try:
        import aiohttp
        
        bot_token = SOCIAL_CONFIG["telegram"]["bot_token"]
        chat_id = SOCIAL_CONFIG["telegram"]["chat_id"]
        
        if not bot_token or not chat_id:
            print("  ⚠️ Telegram: Missing credentials")
            return False
        
        message = get_share_message(url, "telegram")
        
        api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False,
        }
        
        async with session.post(api_url, json=payload) as resp:
            if resp.status == 200:
                print(f"  ✅ Posted to Telegram!")
                return True
            else:
                print(f"  ❌ Telegram error: {resp.status}")
                return False
                
    except Exception as e:
        print(f"  ❌ Telegram error: {e}")
        return False

async def post_to_discord(url: str, session) -> bool:
    """Post to Discord via webhook"""
    if not SOCIAL_CONFIG["discord"]["enabled"]:
        return False
    
    try:
        import aiohttp
        
        webhook_url = SOCIAL_CONFIG["discord"]["webhook_url"]
        if not webhook_url:
            print("  ⚠️ Discord: No webhook URL configured")
            return False
        
        message = get_share_message(url, "discord")
        
        payload = {
            "content": message,
            "username": "Cadbury Secret Santa Monitor",
            "avatar_url": "https://www.cadbury.co.uk/favicon.ico",
        }
        
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 204:
                print(f"  ✅ Posted to Discord!")
                return True
            else:
                print(f"  ❌ Discord error: {resp.status}")
                return False
                
    except Exception as e:
        print(f"  ❌ Discord error: {e}")
        return False

async def post_to_slack(url: str, session) -> bool:
    """Post to Slack via webhook"""
    if not SOCIAL_CONFIG["slack"]["enabled"]:
        return False
    
    try:
        import aiohttp
        
        webhook_url = SOCIAL_CONFIG["slack"]["webhook_url"]
        if not webhook_url:
            print("  ⚠️ Slack: No webhook URL configured")
            return False
        
        message = get_share_message(url, "slack")
        
        payload = {
            "text": message,
            "username": "Cadbury Monitor",
            "icon_emoji": ":chocolate_bar:",
        }
        
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status == 200:
                print(f"  ✅ Posted to Slack!")
                return True
            else:
                print(f"  ❌ Slack error: {resp.status}")
                return False
                
    except Exception as e:
        print(f"  ❌ Slack error: {e}")
        return False

async def post_to_mastodon(url: str, session) -> bool:
    """Post to Mastodon"""
    if not SOCIAL_CONFIG["mastodon"]["enabled"]:
        return False
    
    try:
        import aiohttp
        
        instance = SOCIAL_CONFIG["mastodon"]["instance_url"]
        access_token = SOCIAL_CONFIG["mastodon"]["access_token"]
        
        if not access_token or not instance:
            print("  ⚠️ Mastodon: Missing credentials")
            return False
        
        message = get_share_message(url, "mastodon")
        
        api_url = f"{instance}/api/v1/statuses"
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {"status": message, "visibility": "public"}
        
        async with session.post(api_url, json=payload, headers=headers) as resp:
            if resp.status == 200:
                print(f"  ✅ Posted to Mastodon!")
                return True
            else:
                print(f"  ❌ Mastodon error: {resp.status}")
                return False
                
    except Exception as e:
        print(f"  ❌ Mastodon error: {e}")
        return False

async def post_to_bluesky(url: str, session) -> bool:
    """Post to Bluesky"""
    if not SOCIAL_CONFIG["bluesky"]["enabled"]:
        return False
    
    try:
        import aiohttp
        
        handle = SOCIAL_CONFIG["bluesky"]["handle"]
        app_password = SOCIAL_CONFIG["bluesky"]["app_password"]
        
        if not handle or not app_password:
            print("  ⚠️ Bluesky: Missing credentials")
            return False
        
        # Create session
        session_url = "https://bsky.social/xrpc/com.atproto.server.createSession"
        session_data = {"identifier": handle, "password": app_password}
        
        async with session.post(session_url, json=session_data) as resp:
            session_response = await resp.json()
            access_token = session_response.get("accessJwt")
        
        if not access_token:
            print("  ❌ Bluesky: Failed to authenticate")
            return False
        
        # Create post
        message = get_share_message(url, "bluesky")
        
        post_url = "https://bsky.social/xrpc/com.atproto.repo.createRecord"
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "repo": session_response["did"],
            "collection": "app.bsky.feed.post",
            "record": {
                "text": message,
                "createdAt": datetime.now().isoformat(),
                "$type": "app.bsky.feed.post",
            },
        }
        
        async with session.post(post_url, json=payload, headers=headers) as resp:
            if resp.status == 200:
                print(f"  ✅ Posted to Bluesky!")
                return True
            else:
                print(f"  ❌ Bluesky error: {resp.status}")
                return False
                
    except Exception as e:
        print(f"  ❌ Bluesky error: {e}")
        return False

async def share_to_all_platforms(url: str):
    """Share to all enabled social media platforms"""
    print(f"\n📢 Sharing to social media platforms...")
    
    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            tasks = [
                post_to_twitter(url, session),
                post_to_facebook(url, session),
                post_to_linkedin(url, session),
                post_to_reddit(url, session),
                post_to_telegram(url, session),
                post_to_discord(url, session),
                post_to_slack(url, session),
                post_to_mastodon(url, session),
                post_to_bluesky(url, session),
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            success_count = sum(1 for r in results if r is True)
            print(f"\n📊 Shared successfully to {success_count} platform(s)")
            
    except ImportError:
        print("  ⚠️ aiohttp not installed. Install with: pip install aiohttp")
        print("  📱 Opening manual share links instead...")
        open_manual_share_links(url)

def open_manual_share_links(url: str):
    """Open manual share links in browser if API keys not configured"""
    encoded_url = quote(url)
    message = quote(get_share_message(url, "twitter"))
    
    share_urls = [
        f"https://twitter.com/intent/tweet?text={message}",
        f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}",
        f"https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}",
        f"https://reddit.com/submit?url={encoded_url}&title={quote('Cadbury Secret Santa - Free Chocolate!')}",
        f"https://api.whatsapp.com/send?text={message}",
    ]
    
    print(f"  🌐 Opening {len(share_urls)} manual share windows...")
    for share_url in share_urls:
        webbrowser.open(share_url)

# ============================================================================
# URL CHECKING
# ============================================================================

async def check_url_real_browser(url: str, page) -> str:
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        final_url = page.url
        return final_url
    except Exception as e:
        return f"Error: {e}"

# ============================================================================
# MAIN MONITORING LOOP
# ============================================================================

async def monitor_links(interval: int = 60, jitter: int = 15):
    print("🎅 Cadbury Secret Santa Monitor with Social Auto-Share")
    print(f"📢 Credit: {CREDIT_HANDLE} ({CREDIT_URL})")
    print("=" * 70)
    
    # Show enabled platforms
    enabled_platforms = [name for name, config in SOCIAL_CONFIG.items() if config["enabled"]]
    if enabled_platforms:
        print(f"✅ Enabled platforms: {', '.join(enabled_platforms)}")
    else:
        print("⚠️ No API keys configured - will use manual sharing")
    
    print("\nPress Ctrl+C to stop.\n")

    def signal_handler():
        print("\n🛑 Stopping...")
        asyncio.get_event_loop().stop()

    signal.signal(signal.SIGINT, lambda s, f: signal_handler())

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="en-GB",
        )
        page = await context.new_page()

        while True:
            new_active_found = False

            for url in urls:
                print(f"Checking → {url}")
                final_url = await check_url_real_browser(url, page)

                if not final_url.startswith("http"):
                    print(f"  ⚠️ Failed: {final_url}")
                    continue

                if BAD_URL_CONTAINS in final_url.lower():
                    print(f"  ❌ Still missed out")
                    continue

                normalized = urlparse(final_url)._replace(query="").geturl()

                if normalized not in opened_destinations:
                    print(f"  ✅🎉 NEW ACTIVE LINK DETECTED!")
                    print(f"     → {final_url}")
                    
                    # Open in browser
                    webbrowser.open(final_url)
                    opened_destinations.add(normalized)
                    
                    # Share to social media
                    await share_to_all_platforms(final_url)
                    
                    new_active_found = True
                else:
                    print(f"  🔁 Already opened before")

            if not new_active_found:
                print("  ⏳ No new active links found this round.")

            sleep_time = interval + random.randint(-jitter, jitter)
            print(f"  😴 Sleeping {sleep_time} seconds...\n")
            await asyncio.sleep(sleep_time)

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🎅 CADBURY SECRET SANTA SOCIAL AUTO-SHARE MONITOR")
    print("=" * 70)
    print(f"\n📢 All posts credit: {CREDIT_HANDLE}")
    print(f"🔗 {CREDIT_URL}\n")
    
    asyncio.run(monitor_links(interval=60, jitter=15))
