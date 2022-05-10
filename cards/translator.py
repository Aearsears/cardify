import requests
import json
import os
import asyncio
import urllib.parse
from threading import Thread
from pyppeteer import launch

asyncio.set_event_loop(asyncio.new_event_loop())

EXEC_PATH = os.environ.get(
    "GOOGLE_CHROME_SHIM", None)

ML_LINK = os.environ.get(
    "ML_LINK", "https://share.streamlit.io/aearsears/streamlit-qa-generator/main?text=")


def get_questions(text):
    # takes in dict of {"text": "this is that. that is this."}
    new_thread = Thread(target=between_callback, args=(text,))
    new_thread.start()
    new_thread.join()
    return True


def between_callback(args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(task(args))
    loop.close()


async def task(data):
    print(data)
    mlLink = ML_LINK + \
        urllib.parse.quote(data["text"])
    browser = await launch(handleSIGINT=False,
                           handleSIGTERM=False,
                           handleSIGHUP=False,
                           headless=True,
                           executablePath=EXEC_PATH,
                           autoClose=False,
                           args=['--no-sandbox']
                           )
    page = await browser.newPage()
    await page.goto(mlLink, waitUntil="networkidle0")
    await page.content()
    elementHandle = await page.waitForSelector('div#root>div>div>div>iframe')
    frame = await elementHandle.contentFrame()
    # wait until the desired box appears
    await frame.waitForSelector('h1#status-code')
    await browser.close()
