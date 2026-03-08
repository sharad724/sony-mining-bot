"""
Firebase Database Connection aur Operations
"""

import firebase_admin
from firebase_admin import credentials, db
import json
import os
import time
from datetime import datetime
import config

# Firebase connection
def init_firebase():
    """Firebase se connection banata hai"""
    try:
        # Environment se service account lo
        service_account = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
        if not service_account:
            print("❌ Firebase service account not found!")
            return None
        
        # JSON parse karo
        cred_info = json.loads(service_account)
        cred = credentials.Certificate(cred_info)
        
        # Firebase initialize karo
        firebase_admin.initialize_app(cred, {
            'databaseURL': config.FIREBASE_DATABASE_URL
        })
        
        print("✅ Firebase connected!")
        return db.reference('/')
        
    except Exception as e:
        print(f"❌ Firebase error: {e}")
        return None

# Global reference
db_ref = init_firebase()

# ============= USER FUNCTIONS =============

def get_user(user_id):
    """User ka data Firebase se lao"""
    if not db_ref:
        return None
    return db_ref.child(f'users/{user_id}').get()

def create_user(user_id, username, first_name, referrer=None):
    """Naya user banao"""
    if not db_ref:
        return None
    
    user_data = {
        'user_id': str(user_id),
        'username': username or first_name,
        'first_name': first_name,
        'balance': config.WELCOME_BONUS,
        'mining_rate': config.MINING_RATE,
        'last_claim': int(time.time()),
        'last_withdrawal': 0,
        'referral_count': 0,
        'referral_earnings': 0,
        'total_mined': 0,
        'total_withdrawn': 0,
        'joined_date': datetime.now().isoformat(),
        'referred_by': referrer
    }
    
    db_ref.child(f'users/{user_id}').set(user_data)
    return user_data

def update_user(user_id, data):
    """User data update karo"""
    if not db_ref:
        return False
    db_ref.child(f'users/{user_id}').update(data)
    return True

# ============= MINING FUNCTIONS =============

def claim_mining(user_id):
    """Mining claim process karo"""
    user = get_user(user_id)
    if not user:
        return None
    
    current_time = int(time.time())
    last_claim = user.get('last_claim', current_time)
    time_diff = current_time - last_claim
    
    # 1 ghante mein ek baar mine kar sakte hain
    if time_diff < 3600:
        remaining = 3600 - time_diff
        minutes = remaining // 60
        return {
            'success': False,
            'message': f"⏳ {minutes} minute mein aana"
        }
    
    # Kitne ghante ka reward (max 24 ghante)
    hours = min(time_diff / 3600, config.MAX_MINING_HOURS)
    reward = hours * user.get('mining_rate', config.MINING_RATE)
    
    # User update karo
    new_balance = user.get('balance', 0) + reward
    new_total = user.get('total_mined', 0) + reward
    
    update_user(user_id, {
        'balance': new_balance,
        'last_claim': current_time,
        'total_mined': new_total
    })
    
    return {
        'success': True,
        'reward': round(reward, 2),
        'new_balance': round(new_balance, 2),
        'hours': round(hours, 1)
    }

def get_stats():
    """Bot statistics nikaalo"""
    if not db_ref:
        return {}
    
    users = db_ref.child('users').get() or {}
    
    total_users = len(users)
    total_balance = sum(u.get('balance', 0) for u in users.values())
    total_mined = sum(u.get('total_mined', 0) for u in users.values())
    
    return {
        'total_users': total_users,
        'total_balance': round(total_balance, 2),
        'total_mined': round(total_mined, 2)
  }
