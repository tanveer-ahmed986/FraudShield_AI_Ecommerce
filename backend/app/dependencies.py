from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings

# Configure engine for Supabase connection pooler
engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_size=5,              # Smaller pool for connection pooler
    max_overflow=10,          # Max overflow connections
    pool_pre_ping=True,       # Test connections before using
    pool_recycle=3600,        # Recycle connections after 1 hour
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
