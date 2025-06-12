import asyncio, pandas as pd
from playwright.async_api import async_playwright

async def get_follower_count(username):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Headed mode is less likely to be blocked
        page = await browser.new_page()
        await page.goto(f'https://x.com/{username}', wait_until='networkidle')
        # await page.wait_for_timeout(5000)  # Allow extra time for dynamic content

        # Try to locate the followers link by its accessible name/text
        try:
            # Look for the link containing 'Followers' and get its visible text
            locator = page.locator("a:has-text('Followers')")
            await locator.wait_for(timeout=10000)
            text = await locator.inner_text()
            # Extract the number from the text (e.g., "12.1M Followers")
            count = text.split()[0]
        except Exception:
            # Fallback: try XPath as a backup
            elements = await page.locator('//a[contains(@href,"/followers")]').all()
            count = None
            for el in elements:
                txt = await el.inner_text()
                if "Follower" in txt:
                    count = txt.split()[0]
                    break
            if not count:
                count = "Follower count not found"
        await browser.close()
        return count

if __name__ == "__main__":
    df = pd.read_csv("behaviour_simulation_train.csv", encoding='cp1252')
    follower_map = dict()
    for username in df['username'].unique():
        count = asyncio.run(get_follower_count(username))
        count = count.replace(',','')
        if count[-1] == 'M':
            count = int(float(count[:-1]) * 1000000)
        elif count[-1] == 'K':
            count = int(float(count[:-1]) * 1000)
        else:
            count = int(count)

        print(f"{username} has {count} followers.")
        follower_map[username] = count
    df['followers'] = df['username'].map(follower_map)
    df.to_csv("with_followers.csv", index=False)






# import asyncio, pandas as pd
# from playwright.async_api import async_playwright
#
# async def get_follower_count(browser, username, sem):
#     global n
#     async with sem:
#         page = await browser.new_page()
#         try:
#             await page.route('**/*.{png,jpg,jpeg,webp,gif,svg,mp4}', lambda route: route.abort())
#             await page.goto(f'https://x.com/{username}', wait_until='networkidle', timeout=45000)
#
#             locator = page.locator("a:has-text('Followers')")
#             await locator.wait_for(timeout=15000)
#             text = await locator.inner_text()
#
#             count = text.split()[0].replace(',', '')
#             if count[-1] == 'M':
#                 count = int(float(count[:-1]) * 1000000)
#             elif count[-1] == 'K':
#                 count = int(float(count[:-1]) * 1000)
#             else:
#                 count = int(count)
#
#             print(username, count)
#             return {username: count}
#
#         except Exception as e:
#             print(username)
#             return {username: None}
#         finally:
#             await page.close()
#
#
# async def main():
#     df = pd.read_csv("behaviour_simulation_train.csv", encoding='cp1252')
#     sem = asyncio.Semaphore(3)
#
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         results = await asyncio.gather(
#             *[get_follower_count(browser, username, sem)
#               for username in df['username'].unique()]
#         )
#         await browser.close()
#
#     # Process results and save
#     follower_map = {k: v for d in results for k, v in d.items()}
#     df['followers'] = df['username'].map(follower_map)
#     df.to_csv("with_followers.csv", index=False)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())