import discord
from discord.ext import commands, tasks
import yfinance as yf
from datetime import datetime
from dotenv import load_dotenv
import os

# Bot token and channel ID
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
TICKERS = ['AAPL', 'GOOGL', 'MSFT'] # Initial list of ticker symbols to track

# Set up intents for the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

 # Called when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    check_market_status.start()

# Fetch stock information for a given ticker
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    today_data = stock.history(period='1d')
    if today_data.empty:
        # Return default values if no data is available
        return stock.info['shortName'], ticker, None, None, None, None
    # Extract relevant information
    open_price = round(today_data['Open'][0], 4)
    close_price = round(today_data['Close'][0], 4)
    performance = (close_price - open_price) / open_price * 100
    date = today_data.index[0].strftime('%Y-%m-%d')
    return stock.info['shortName'], ticker, open_price, close_price, performance, date

# Periodically check the market status
@tasks.loop(minutes=1)
async def check_market_status():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    # Send updates at market open and close times
    if current_time == "09:30":
        await send_stock_update("Market Open")
    elif current_time == "16:00":
        await send_stock_update("Market Close")

 # Send stock updates to the specified channel
async def send_stock_update(event):
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    for ticker in TICKERS:
        name, ticker, open_price, close_price, performance, date = get_stock_info(ticker)
        if open_price is not None and close_price is not None:
            await channel.send(
                f'{event}\n'
                f'Stock: {name} ({ticker})\n'
                f'Date: {date}\n'
                f'Open Price: {open_price:.4f}\n'
                f'Close Price: {close_price:.4f}\n'
                f'Performance: {performance:.2f}%'
            )
        else:
            await channel.send(f'{event}\nNo data available for {ticker}')

# Command to add a ticker to the tracking list
@bot.command(name='add')
async def add_ticker(ctx, ticker: str):
    if ticker not in TICKERS:
        TICKERS.append(ticker)
        await ctx.send(f'Added {ticker} to the tracking list.')
    else:
        await ctx.send(f'{ticker} is already in the tracking list.')

# Command to remove a ticker from the tracking list
@bot.command(name='remove')
async def remove_ticker(ctx, ticker: str):
    if ticker in TICKERS:
        TICKERS.remove(ticker)
        await ctx.send(f'Removed {ticker} from the tracking list.')
    else:
        await ctx.send(f'{ticker} is not in the tracking list.')

# Command to list all tracked tickers with their information
@bot.command(name='list')
async def list_tickers(ctx):
    response = "Tracked tickers:\n"
    for ticker in TICKERS:
        name, ticker, open_price, close_price, performance, date = get_stock_info(ticker)
        if open_price is not None and close_price is not None:
            response += (
                f'Stock: {name} ({ticker})\n'
                f'Date: {date}\n'
                f'Open Price: {open_price:.4f}\n'
                f'Close Price: {close_price:.4f}\n'
                f'Performance: {performance:.2f}%\n\n'
            )
        else:
            response += f'Stock: {name} ({ticker})\nNo data available\n\n'
    await ctx.send(response)

# Command to get information for a specific ticker
@bot.command(name='info')
async def stock_info(ctx, ticker: str):
    name, ticker, open_price, close_price, performance, date = get_stock_info(ticker)
    if open_price is not None and close_price is not None:
        await ctx.send(
            f'Stock: {name} ({ticker})\n'
            f'Date: {date}\n'
            f'Open Price: {open_price:.4f}\n'
            f'Close Price: {close_price:.4f}\n'
            f'Performance: {performance:.2f}%'
        )
    else:
        await ctx.send(f'No data available for {ticker}')

# Run the bot with the specified token
bot.run(TOKEN)