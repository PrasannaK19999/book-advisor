from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL connection — matches the credentials in docker-compose.yml
SQLALCHEMY_DATABASE_URL = "postgresql://bookadmin:bookpass@localhost:5433/bookadvisor"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency: hands a DB session to an endpoint, then closes it after.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()