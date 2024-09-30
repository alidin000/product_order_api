from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/product_order_db"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session

# # Function to check the connection
# async def check_connection():
#     async with engine.connect() as conn:
#         # Execute a simple SQL query to check the connection
#         result = await conn.execute(text("SELECT version();"))
#         version = result.fetchone()
#         print(f"Database Version: {version[0]}")

# # Running the async function
# import asyncio
# asyncio.run(check_connection())
