# Discord Stock Tracker Bot

A Discord bot that tracks specific stocks and provides updates on their performance.

## Features

- Tracks the opening and closing prices of specified stocks.
- Provides daily updates when the stock market opens and closes.
- Allows users to add and remove tickers from the tracking list.
- Displays information about tracked stocks and other stocks on request.

## Prerequisites

- Python 3.6 or higher
- Discord account and a server where you have permission to add bots
- `python-dotenv` library for loading environment variables

## Usage
Commands<br>
!add <TICKER>: Add a ticker to the tracking list.<br>
!remove <TICKER>: Remove a ticker from the tracking list.<br>
!list: List all tracked tickers with their information.<br>
!info <TICKER>: Get information for a specific ticker.<br>



### Summary

1. **Clone the repository**: `git clone https://github.com/yourusername/discord-stock-tracker-bot.git`
2. **Create and activate a virtual environment**: `python -m venv venv` and `source venv/bin/activate`
3. **Create a `.env` file**: `touch .env` and add your bot token and channel ID
4. **Run the bot**: `python stock_bot.py`

By following this guide, you should be able to set up and run your Discord stock tracker bot easily.
