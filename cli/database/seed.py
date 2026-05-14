import asyncio

from app.db.seeders.__main__ import SEEDERS_TO_RUN

def seed_db():
    for seeder in SEEDERS_TO_RUN:
        asyncio.run(seeder.run())