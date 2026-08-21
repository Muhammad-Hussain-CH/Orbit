from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# The engine: one shared connection to Postgres for the whole app.
engine = create_engine(settings.DATABASE_URL, echo=False)

# A factory that produces new Session objects when called.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The parent class every table model will inherit from.
Base = declarative_base()


# Dependency: yields one session per request, always closes it afterward.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()