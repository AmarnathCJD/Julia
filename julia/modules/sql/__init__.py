from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

DB_URI = "postgres://uemcxpmiublroc:05a41eae1de2eef1d72c68b260d7a0ce3b2155636ebef0bd648c713d2ae86012@ec2-52-70-67-123.compute-1.amazonaws.com:5432/d1qsmgemcfcvj7"


def start() -> scoped_session:
    engine = create_engine(DB_URI, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()
