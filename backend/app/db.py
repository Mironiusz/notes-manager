from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "notes.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
