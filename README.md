# Discord URL Bypass Bot

A Discord bot that automates unlocking protected URLs (e.g., Platoboost, Linkvertise) using a headless browser.

## Features
- Cloudflare bypass using undetected-chromedriver
- Auto-click Continue button
- Extracts redirected URL (loot.link, etc)
- Uses https://bypass.city to fetch final result
- Sends both private and public messages with results

## Setup

1. Clone the repository
2. Create a `.env` file and add your Discord bot token:

```
DISCORD_BOT_TOKEN=your_token_here
```

3. Install dependencies:

```bash
poetry install
```

4. Run the bot:

```bash
python main.py
```

## Commands
- `/bypass <url>`: Starts the bypass automation