"""
Sony Mining Bot - Main Bot File
Telegram par mining ka main program
"""

import logging
import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    ContextTypes
)
import config
import firebase_config as db
from keep_alive import keep_alive

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============= KEYBOARDS (Buttons) =============

def get_main_keyboard():
    """Main menu ke buttons"""
    keyboard = [
        [InlineKeyboardButton("⛏️ Mine", callback_data='mine'),
         InlineKeyboardButton("💰 Balance", callback_data='balance')],
        [InlineKeyboardButton("👥 Refer", callback_data='refer'),
         InlineKeyboardButton("📊 Dashboard", callback_data='dashboard')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    """Wapas jane ka button"""
    keyboard = [[InlineKeyboardButton("🔙 Menu mein wapas", callback_data='menu')]]
    return InlineKeyboardMarkup(keyboard)

# ============= COMMANDS =============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start command - jab koi bot start kare"""
    user = update.effective_user
    user_id = str(user.id)
    
    # Referral check
    args = context.args
    referrer = args[0] if args else None
    
    # User data lo ya naya banao
    user_data = db.get_user(user_id)
    
    if not user_data:
        # Naya user hai
        user_data = db.create_user(user_id, user.username, user.first_name, referrer)
        welcome_text = f"""
🚀 **{config.APP_NAME} mein aapka swagat hai!**

🎁 Aapko mila **{config.WELCOME_BONUS} {config.TOKEN_NAME}** welcome bonus!

💰 **Mining shuru karein:**
• Har ghante mine karein
• {config.MINING_RATE} {config.TOKEN_NAME} per hour
• Referrals se aur bhi bonus

Neeche diye buttons se shuru karein!
        """
    else:
        # Purana user hai
        welcome_text = f"""
🚀 **{config.APP_NAME} mein wapas swagat!**

💰 **Aapka balance:** {user_data.get('balance', 0):.2f} {config.TOKEN_NAME}
⚡ **Mining rate:** {user_data.get('mining_rate')} {config.TOKEN_NAME}/hour
👥 **Referrals:** {user_data.get('referral_count', 0)}

Mining jari rakhein!
        """
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_keyboard(),
        parse_mode='Markdown'
    )

async def mine_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/mine command - mining karne ke liye"""
    user_id = str(update.effective_user.id)
    
    user_data = db.get_user(user_id)
    if not user_data:
        await update.message.reply_text("Pehle /start karein!")
        return
    
    # Mining claim karo
    result = db.claim_mining(user_id)
    
    if result['success']:
        # Random mining messages
        messages = [
            f"⛏️ Mining ho gaya! Mila {result['reward']} {config.TOKEN_NAME}!",
            f"⚡ Hashrate badhi! +{result['reward']} {config.TOKEN_NAME}",
            f"💎 Rare block mila! +{result['reward']} {config.TOKEN_NAME}",
            f"🚀 Boost active! +{result['reward']} {config.TOKEN_NAME}"
        ]
        message = random.choice(messages)
        message += f"\n\n💰 Naya balance: {result['new_balance']} {config.TOKEN_NAME}"
    else:
        message = result['message']
    
    await update.message.reply_text(message, reply_markup=get_back_keyboard())

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/balance command - balance dekhne ke liye"""
    user_id = str(update.effective_user.id)
    user_data = db.get_user(user_id)
    
    if not user_data:
        await update.message.reply_text("Pehle /start karein!")
        return
    
    # Mining status
    last_claim = user_data.get('last_claim', 0)
    current_time = int(time.time())
    time_diff = current_time - last_claim
    
    if time_diff < 3600:
        remaining = 3600 - time_diff
        minutes = remaining // 60
        mining_status = f"⏳ Agli mine: {minutes} minute mein"
    else:
        mining_status = "✅ Mine kar sakte ho!"
    
    balance_text = f"""
💰 **Aapka {config.APP_NAME} Wallet**

**{config.TOKEN_NAME} Balance:** {user_data.get('balance', 0):.2f}
⚡ **Mining Rate:** {user_data.get('mining_rate')}/hour
📊 **Total Mined:** {user_data.get('total_mined', 0):.2f}
👥 **Referrals:** {user_data.get('referral_count', 0)}

⛏️ **Status:** {mining_status}
    """
    
    await update.message.reply_text(balance_text, reply_markup=get_back_keyboard())

async def refer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/refer command - referral link ke liye"""
    user_id = str(update.effective_user.id)
    
    # Bot ka username lo
    bot = await context.bot.get_me()
    referral_link = f"https://t.me/{bot.username}?start={user_id}"
    
    refer_text = f"""
👥 **Referral Program**

**Aapka referral link:**
`{referral_link}`

**Kaise kaam karta hai:**
• Har referral par {config.REFERRAL_BONUS} {config.TOKEN_NAME} milega
• Referrals ki mining ka {config.REFERRAL_PERCENTAGE}% bonus
• Koi limit nahi!

Link copy karo aur dosto ko bhejo!
    """
    
    await update.message.reply_text(
        refer_text,
        reply_markup=get_back_keyboard(),
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/help command - madad ke liye"""
    help_text = f"""
📚 **{config.APP_NAME} Help Center**

**Commands:**
/start - Main menu
/mine - Mining karo
/balance - Balance dekho
/refer - Referral link lo
/help - Yeh menu

**Mining Rules:**
• Har ghante mine kar sakte ho
• {config.MINING_RATE} {config.TOKEN_NAME} per hour
• 24 ghante accumulate kar sakte ho

**Referral:**
• {config.REFERRAL_BONUS} {config.TOKEN_NAME} per referral
• 10% bonus unki mining se

**Support:** {config.SUPPORT_GROUP}
    """
    
    await update.message.reply_text(help_text, reply_markup=get_back_keyboard())

# ============= BUTTON HANDLERS =============

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Button click handle karta hai"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = str(update.effective_user.id)
    
    if data == 'menu':
        await query.edit_message_text(
            "Main Menu:",
            reply_markup=get_main_keyboard()
        )
    
    elif data == 'mine':
        result = db.claim_mining(user_id)
        
        if result['success']:
            message = f"✅ Mila {result['reward']} {config.TOKEN_NAME}!"
            message += f"\n💰 Naya balance: {result['new_balance']} {config.TOKEN_NAME}"
        else:
            message = result['message']
        
        await query.edit_message_text(message, reply_markup=get_back_keyboard())
    
    elif data == 'balance':
        user_data = db.get_user(user_id)
        if user_data:
            text = f"💰 Balance: {user_data.get('balance', 0):.2f} {config.TOKEN_NAME}"
        else:
            text = "Pehle /start karein!"
        
        await query.edit_message_text(text, reply_markup=get_back_keyboard())
    
    elif data == 'refer':
        bot = await context.bot.get_me()
        link = f"https://t.me/{bot.username}?start={user_id}"
        text = f"👥 Aapka referral link:\n`{link}`"
        await query.edit_message_text(text, reply_markup=get_back_keyboard(), parse_mode='Markdown')
    
    elif data == 'dashboard':
        dashboard_url = "https://sony-mining.netlify.app"
        await query.edit_message_text(
            f"📊 **Web Dashboard**\n\n"
            f"Yahan jao: {dashboard_url}?userId={user_id}\n\n"
            f"Apna Telegram ID: `{user_id}`",
            reply_markup=get_back_keyboard(),
            parse_mode='Markdown'
        )
    
    elif data == 'help':
        await help_command(update, context)

# ============= ADMIN COMMANDS =============

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin ke liye statistics"""
    user_id = str(update.effective_user.id)
    
    # Check if admin
    if user_id not in [str(a) for a in config.ADMIN_IDS]:
        await update.message.reply_text("❌ Sirf admin use kar sakta hai!")
        return
    
    stats = db.get_stats()
    
    text = f"""
📊 **Bot Statistics**

👥 Total Users: {stats.get('total_users', 0)}
💰 Total Balance: {stats.get('total_balance', 0)} {config.TOKEN_NAME}
⛏️ Total Mined: {stats.get('total_mined', 0)} {config.TOKEN_NAME}
    """
    
    await update.message.reply_text(text, parse_mode='Markdown')

# ============= MAIN FUNCTION =============

def main():
    """Bot start karne ka main function"""
    
    # Bot token lo
    token = os.environ.get('BOT_TOKEN')
    if not token:
        logger.error("❌ BOT_TOKEN environment mein nahi mila!")
        return
    
    # Application banao
    app = Application.builder().token(token).build()
    
    # Commands add karo
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mine", mine_command))
    app.add_handler(CommandHandler("balance", balance_command))
    app.add_handler(CommandHandler("refer", refer_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # Admin commands
    app.add_handler(CommandHandler("stats", admin_stats))
    
    # Button handler
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Web server for 24/7
    keep_alive()
    
    # Bot start karo
    logger.info(f"🚀 {config.APP_NAME} Bot starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
