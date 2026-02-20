"""CLI script to initialise the Neon Postgres schema."""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.services.db import init_db


async def main() -> None:
    await init_db()
    print("✅ Table conversation_turns created (or already exists)")


if __name__ == "__main__":
    asyncio.run(main())
