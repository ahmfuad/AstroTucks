#!/usr/bin/env python
"""
AstroTucks Telegram Bot adapted for Azure deployment using Flask and python-telegram-bot v20+
"""

import logging
import os
import requests
import dateparser
import pytz
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
from flask import Flask, request

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# States
LOCATION1, LOCATION2 = range(2)

# Initialize Flask app
app = Flask(__name__)

# Get token from environment variable for security
TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text('Yes Boss! I\'m awake 🤓')

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to the hello command."""
    await update.message.reply_text(f'Hey There {update.message.from_user.first_name} :D')

async def sunrise(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the sunrise conversation."""
    location_keyboard = KeyboardButton(text="Share Location", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[location_keyboard]], one_time_keyboard=True)
    
    await update.message.reply_text(
        'Please share your location so I can calculate the sunrise time:',
        reply_markup=reply_markup
    )
    return LOCATION1

async def sunset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the sunset conversation."""
    location_keyboard = KeyboardButton(text="Share Location", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[location_keyboard]], one_time_keyboard=True)
    
    await update.message.reply_text(
        'Please share your location so I can calculate the sunset time:',
        reply_markup=reply_markup
    )
    return LOCATION2

async def location1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle location to calculate sunrise time."""
    try:
        user_location = update.message.location
        lat, lng = user_location.latitude, user_location.longitude
        BDT = pytz.timezone('Asia/Dhaka')

        URL = "https://api.sunrise-sunset.org/json"
        PARAMS = {'lat': lat, 'lng': lng, 'formatted': '1'}

        r = requests.get(url=URL, params=PARAMS)
        r.raise_for_status()  # Check for errors in the request
        data = r.json()

        dt = dateparser.parse(data["results"]["sunrise"])
        dt = dt.astimezone(BDT)
        dt = dt.strftime("%I:%M:%S %p")

        await update.message.reply_text(
            f"📍 Location Coordinates:\n\n"
            f"Latitude: {lat}\n"
            f"Longitude: {lng}\n\n"
            f"Next Sunrise Time is: {dt}",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        logger.error(f"Error calculating sunrise: {e}")
        await update.message.reply_text('Sorry, I encountered an error. Please try again later.', reply_markup=ReplyKeyboardRemove())
    
    return ConversationHandler.END

async def location2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle location to calculate sunset time."""
    try:
        user_location = update.message.location
        lat, lng = user_location.latitude, user_location.longitude
        BDT = pytz.timezone('Asia/Dhaka')

        URL = "https://api.sunrise-sunset.org/json"
        PARAMS = {'lat': lat, 'lng': lng, 'formatted': '1'}

        r = requests.get(url=URL, params=PARAMS)
        r.raise_for_status()  # Check for errors in the request
        data = r.json()

        dt = dateparser.parse(data["results"]["sunset"])
        dt = dt.astimezone(BDT)
        dt = dt.strftime("%I:%M:%S %p")

        await update.message.reply_text(
            f"📍 Location Coordinates:\n\n"
            f"Latitude: {lat}\n"
            f"Longitude: {lng}\n\n"
            f"Sunset Time Today is: {dt}",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        logger.error(f"Error calculating sunset: {e}")
        await update.message.reply_text('Sorry, I encountered an error. Please try again later.', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel and end the conversation."""
    await update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Create application
application = Application.builder().token(TOKEN).build()

# Add conversation handlers
sunrise_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('sunrise', sunrise)],
    states={LOCATION1: [MessageHandler(filters.LOCATION, location1)]},
    fallbacks=[CommandHandler('cancel', cancel)],
)

sunset_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('sunset', sunset)],
    states={LOCATION2: [MessageHandler(filters.LOCATION, location2)]},
    fallbacks=[CommandHandler('cancel', cancel)],
)

# Add handlers to application
application.add_handler(sunrise_conv_handler)
application.add_handler(sunset_conv_handler)
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('hello', hello))

# Flask route for webhook
@app.route('/webhook', methods=['POST'])
async def webhook():
    """Handle webhook updates from Telegram."""
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
    except Exception as e:
        logger.error(f"Error processing update: {e}")
    return "OK"

# Set webhook route
@app.route('/set_webhook', methods=['GET', 'POST'])
async def set_webhook():
    """Set the bot webhook."""
    try:
        success = await application.bot.set_webhook(WEBHOOK_URL)
        return "Webhook setup ok" if success else "Webhook setup failed"
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return "Webhook setup failed"


# Default route
@app.route('/')
async def index():
    return "Sunrise Sunset Telegram Bot"

# Main function
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))
