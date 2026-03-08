"""
Bot ko 24/7 chalane ke liye Flask server
"""

from flask import Flask
from threading import Thread
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Sony Mining Bot is running 24/7!"

@app.route('/health')
def health():
    return "✅ Bot healthy"

def run():
    """Flask server chalane ke liye"""
    try:
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        logger.error(f"Server error: {e}")

def keep_alive():
    """Server ko alag thread mein chalata hai"""
    t = Thread(target=run)
    t.daemon = True
    t.start()
    logger.info("🌐 Web server started for 24/7 uptime")
