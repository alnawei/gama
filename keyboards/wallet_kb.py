from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_wallet_main_keyboard() -> ReplyKeyboardMarkup:
    """私聊界面的底部常驻按键映射"""
    kb = [
        [KeyboardButton(text="💰 个人中心"), KeyboardButton(text="💳 充值提现")],
        [KeyboardButton(text="📊 账单明细"), KeyboardButton(text="❓ 帮助中心")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_deposit_withdraw_keyboard() -> InlineKeyboardMarkup:
    """充值提现内联悬浮按键"""
    buttons = [
        [
            InlineKeyboardButton(text="📥 快速充值", callback_data="wallet_deposit"),
            InlineKeyboardButton(text="📤 申请提现", callback_data="wallet_withdraw")
        ],
        [InlineKeyboardButton(text="🔄 刷新余额", callback_data="wallet_refresh")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
