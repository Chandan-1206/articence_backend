import asyncio
from app.database import engine

async def main():
    async with engine.begin() as conn:
        print("DB connection OK")

if __name__ == "__main__":
    asyncio.run(main())
