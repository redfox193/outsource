from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://udk2brrhb1kgjr:p980ff8b4006876bf2e260c0b59b2b2192b0aff471072c6e7474f87e7b75ae428@cah8ha8ra8h8i7.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d9sthtpgnn7eb0"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


try:
    engine.connect()
    print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")
