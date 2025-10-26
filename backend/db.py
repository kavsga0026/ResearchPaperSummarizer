from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# SQLite file in this folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./summaries.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=True)
    summary = Column(Text, nullable=False)
    mode = Column(String, default="Normal")   # "Normal" or "ExplainLike10"
    created_at = Column(DateTime, default=datetime.utcnow)
