from typing import Optional, List
from os import getenv
from dotenv import load_dotenv, find_dotenv

from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine, Session,select, Relationship




load_dotenv(find_dotenv())
postgres_url = getenv("DATA_BASE_URL")


app:FastAPI = FastAPI()


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None


class HeroRead(SQLModel):
    id: int
    name: str
    secret_name: str
    age: Optional[int] = None

engine = create_engine(postgres_url, echo=True) 





def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/", response_model=HeroRead)
def create_hero(hero: HeroCreate):
    with Session(engine) as session:
        db_hero = Hero.model_validate(hero)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero


@app.get("/heroes/", response_model=List[HeroRead])
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes