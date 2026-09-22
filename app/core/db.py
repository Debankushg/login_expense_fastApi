from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL="postgresql://debankush:12345@localhost:5432/expense_db"
# postgresql://debankush:12345@localhost:5432/blogdb

# create engine
engine=create_engine(
    DATABASE_URL
    # connect_args={"check_same_thread":False}
)
# create session
SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# dependency (function is used as fastapi dependency)
def get_db():
    db=SessionLocal()
    try:
        #  this gives the session to fastapi
        yield db
    finally:
        db.close()

Base= declarative_base()