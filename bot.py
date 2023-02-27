import os
import discord
import requests
import asyncio
from bs4 import BeautifulSoup
from discord import Intents

intents = Intents.default()
intents.members = True  # Enable the Members intent

client = discord.Client(intents=discord.Intents.all())
ASURA_URL = "https://www.asurascans.com/"
REAPER_URL = "https://reaperscans.com/"

MREADER_URL = "https://www.mreader.co/jumbo/manga/"

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    
    while True:
        asura_chapter = get_latest_chapter(ASURA_URL)
        reaper_chapter = get_latest_chapter(REAPER_URL)

        if asura_chapter is not None:
            await client.wait_until_ready()
            await client.get_channel(1075279391992598591).send(f"Asura Scans released chapter {asura_chapter}.")
        if reaper_chapter is not None:
            await client.wait_until_ready()
            await client.get_channel(1075279391992598591).send(f"Reaper Scans released chapter {reaper_chapter}.")

        await asyncio.sleep(60)

@client.event
async def on_message(message):

 
    print(repr(message.content))
    if message.content == '.ping':
   
        mreader_manga_list = get_most_viewed_manga(MREADER_URL)
        await client.get_channel(1075279391992598591).send(f"Most viewed manga on mreader today:\n\n{mreader_manga_list}")

def get_latest_chapter(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    chapter_div = soup.find("div", class_="chaplist")

    if chapter_div is None:
        return None

    latest_chapter = chapter_div.find("a").text.strip()
    latest_chapter_date = chapter_div.find("span").text.strip()

    # Check if the latest chapter has already been announced
    announced_chapters = load_announced_chapters()
    if latest_chapter in announced_chapters:
        return None

    # Store the latest chapter in the announced chapters list
    announced_chapters.append(latest_chapter)
    save_announced_chapters(announced_chapters)

    return latest_chapter

def get_most_viewed_manga(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    section_body_div = soup.find("div", class_="section-body")

    if section_body_div is None:
        return None

    manga_items = section_body_div.find("ul", class_="swiper-wrapper").find_all("li", class_="swiper-slide novel-item")
    mreader_manga_list = ""

    for manga_item in manga_items:
        manga_title = manga_item.find("a").text.strip()
    
        manga_image_url = manga_item.find("figure", class_="novel-cover").find("img")['src']
        mreader_manga_list += f"{manga_title} ({manga_image_url})\n"

      

    return mreader_manga_list


def load_announced_chapters():
    if not os.path.exists("announced_chapters.txt"):
        return []

    with open("announced_chapters.txt", "r") as f:
        return f.read().splitlines()

def save_announced_chapters(announced_chapters):
    with open("announced_chapters.txt", "w") as f:
        f.write("\n".join(announced_chapters))

client.run("MTA3OTQ0Mjg2MjI1ODc4NjM3NA.GZ45sF.LKSScZGx7TEx3u7V9KPlw6UKkoSwHZFSOWh6QI")
