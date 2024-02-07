from typing import Optional, List
from os import getenv
from dotenv import load_dotenv, find_dotenv

from fastapi import FastAPI, HTTPException,Query,Depends
from sqlmodel import Field, SQLModel, create_engine, Session,select, Relationship




load_dotenv(find_dotenv())
postgres_url = getenv("DATA_BASE_URL")


app:FastAPI = FastAPI()


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class HeroCreate(HeroBase):
    pass


class HeroRead(HeroBase):
    id: int


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None


engine = create_engine(postgres_url, echo=True) 





def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def get_session():
    with Session(engine) as session:
        yield session




@app.post("/heroes/", response_model=HeroRead)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
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
    

@app.get("/hereos/{hero_id}", response_model=HeroRead)
def get_hero(hero_id:int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code= 404, detail="Hero not found")
        return hero
    
@app.get("/hereos/", response_model=List[HeroRead])
def get_hero(offset:int=0, limit:int = Query(default=3, le=30) ):
    with Session(engine) as session:
        heros = session.exec(select(Hero).offset(offset).limit(limit)).all()
        return heros


@app.patch("/hereos/{hero_id}", response_model=HeroRead)
def get_hero(hero_id:int, hero:HeroUpdate):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code= 404, detail="Hero not found")
        hero_data = hero.model_dump(exclude_unset=True)
        for key, value in hero_data.items():
            setattr(hero, key, value)
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero 
    


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(hero)
        session.commit()
        return {"ok": True}
