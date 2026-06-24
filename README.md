game_system/
├── .env
├── main.py
├── core/
│   ├── __init__.py
│   └── config.py
├── database/
│   ├── __init__.py
│   └── session.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── user.py
│   ├── red_packet.py
│   ├── transaction.py
│   └── dealer_bot.py
├── keyboards/
│   ├── __init__.py
│   ├── wallet_kb.py
│   └── admin_kb.py
├── routers/
│   ├── __init__.py
│   ├── wallet_router.py
│   ├── admin_router.py
│   └── dealer_router.py
└── middlewares/
    ├── __init__.py
    ├── rate_limit.py
    └── blacklist.py
