import discord
from discord import app_commands
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import asyncio
import time
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {bot.user}')

@tree.command(name="bypass", description="Bypass protected link")
@app_commands.describe(link="Enter the protected URL")
async def bypass_command(interaction: discord.Interaction, link: str):
    await interaction.response.send_message("Bypassing started...", ephemeral=True)
    start = time.time()

    print("Opened Headless Browser")
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    try:
        driver.get(link)
        print("anti bot bypassed")

        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'continue')]")))
        continue_button.click()
        await asyncio.sleep(3)

        driver.switch_to.window(driver.window_handles[-1])
        redirected_url = driver.current_url
        print(f"Redirected Link: {redirected_url}")

        driver.execute_script("window.open('https://bypass.city');")
        driver.switch_to.window(driver.window_handles[-1])
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea"))).send_keys(redirected_url)
        print("Using Bypass.city")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Bypass Link!')]"))).click()

        result_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Copy Result')]")))
        result_button.click()
        result = driver.find_element(By.TAG_NAME, "textarea").get_attribute("value")

        elapsed = round(time.time() - start, 2)
        response_private = f"| Results: {result} | RLink: {redirected_url} | Time: {elapsed}s |"
        response_public = f"| Url whitelisted | Time: {elapsed}s |"

        await interaction.followup.send(content=response_private, ephemeral=True)
        await interaction.channel.send(content=response_public)

    except Exception as e:
        print("Error:", e)
        await interaction.followup.send("An error occurred while bypassing the link.", ephemeral=True)
    finally:
        driver.quit()

bot.run(TOKEN)