import os
import time
import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from flask import Flask
from threading import Thread

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
AI_KEY = os.getenv("AI_KEY")  # Reserved if AI analysis is needed

# Setup Discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

# Background Flask web server for Render or Railway to keep bot alive
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Start the Flask server in background
Thread(target=run_flask).start()

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def bypass(ctx, link: str):
    start_time = time.time()
    await ctx.reply("🔄 Processing your link...")

    try:
        # Setup undetected Chrome
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(options=options)
        print("🌐 Opened Headless Browser")
        driver.get(link)

        time.sleep(5)
        print("🛡️ Bypassing Cloudflare...")

        # Wait for 'Continue' button
        try:
            continue_button = driver.find_element(By.XPATH, "//button[contains(text(),'Continue')]")
            continue_button.click()
            print("➡️ Clicked Continue Button")
            time.sleep(7)
        except Exception as e:
            print("❌ Couldn't find continue button:", e)

        # Grab redirected URL from new tab or current URL
        redirected_url = driver.current_url
        if "about:blank" in redirected_url:
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            redirected_url = driver.current_url

        print("🔁 Redirected Link:", redirected_url)

        # Open bypass.city
        driver.execute_script("window.open('https://bypass.city');")
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(5)

        # Paste link and click "Bypass Link!"
        input_box = driver.find_element(By.XPATH, "//input[@placeholder='Paste the link here']")
        input_box.send_keys(redirected_url)
        time.sleep(1)
        input_box.send_keys(Keys.ENTER)
        print("🚀 Using Bypass.city")

        # Wait for results and click Copy
        time.sleep(10)
        copy_button = driver.find_element(By.XPATH, "//button[contains(text(),'Copy Result')]")
        copy_button.click()
        time.sleep(1)

        # Get result from input box
        result_url = driver.find_element(By.XPATH, "//input[@id='result']").get_attribute("value")
        total_time = round(time.time() - start_time, 2)

        # Send private and public response
        await ctx.author.send(f"| ✅ **Results**: {result_url}\n| 🔗 RLink: {redirected_url}\n| ⏱️ Time: {total_time}s\n| 🤖 Bot: `{bot.user.name}`")
        await ctx.reply(f"✅ Url whitelisted | Time: {total_time}s")

    except Exception as e:
        await ctx.reply(f"❌ Error: {str(e)}")
        print("❌ Exception:", e)

    finally:
        try:
            driver.quit()
        except:
            pass

# Start the bot
bot.run(DISCORD_BOT_TOKEN)
