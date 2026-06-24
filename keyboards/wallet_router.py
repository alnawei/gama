from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import wallet_kb

# 实例化单独的钱包路由
wallet_router = Router(name="wallet_router")

@wallet_router.message(F.text == "/start")
async def cmd_start(message: Message):
    """处理新用户私聊钱包机器人的启动消息"""
    await message.answer(
        "👋 欢迎使用分布式积分钱包系统！\n在这里您可以安全地管理您的积分与收发流水。",
        reply_markup=wallet_kb.get_wallet_main_keyboard()
    )

@wallet_router.message(F.text == "💰 个人中心")
async def show_profile(message: Message):
    """展示账户余额 (此处预留数据查询，不做业务计算)"""
    # 模拟数据，实际开发中建议在此调用服务层(services)读取
    balance = 0.0000
    frozen = 0.0000
    
    text = (
        f"👤 <b>用户信息</b>\n"
        f"ID: <code>{message.from_user.id}</code>\n\n"
        f"可用积分: <code>{balance:.4f}</code> pts\n"
        f"冻结积分: <code>{frozen:.4f}</code> pts"
    )
    await message.answer(
        text, 
        parse_mode="HTML", 
        reply_markup=wallet_kb.get_deposit_withdraw_keyboard()
    )

@wallet_router.callback_query(F.data == "wallet_refresh")
async def handle_refresh(callback: CallbackQuery):
    """处理刷新余额按键回调"""
    # 此处可再次读取数据库
    await callback.answer("余额已更新 (演示模式)")
