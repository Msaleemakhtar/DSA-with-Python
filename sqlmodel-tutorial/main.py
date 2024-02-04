from typing import Optional, List

from sqlmodel import Field, SQLModel, create_engine, Session,select, Relationship

from dotenv import load_dotenv, find_dotenv
from os import getenv




load_dotenv(find_dotenv)



class Team(SQLModel, table= True):
    id:Optional[int] = Field(default=None, primary_key=True)
    name :str = Field(index=True)
    headdquarters : str
    heroes:List["Hero"] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int]= Field(default=None, foreign_key="team.id")

    team:Optional[Team] = Relationship(back_populates="heroes")



Postgess_url = getenv("DATA_BASE_URL")
engine = create_engine(Postgess_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_hero():
    with Session(engine) as session:
        team_preventer = Team(name="preventer", headdquarters="sharp Tower")
        team__z_force = Team(name="z force", headdquarters="sister Margarate force")

        # session.add(team_preventer)
        # session.add(team__z_force)
        # session.commit()

        hero_deadpond = Hero(name="Deadpond", secret_name="Dive wilson", team_id=team_preventer.id)
        hero_rusty_man = Hero(name="RustyMan", secret_name="Tommy Sharp", age=48, team_id=team__z_force.id)
        hero_spider_man= Hero(name="SpiderBoy", secret_name="Pedro parker", age=32)

        # session.add(hero_deadpond)
        # session.add(hero_rusty_man)
        # session.add(hero_spider_man)

        # session.commit()

        # session.refresh(hero_deadpond)
        # session.refresh(hero_rusty_man)
        # session.refresh(hero_spider_man)

        # print("hero_deadpond", hero_deadpond)
        # print("rudty_hero", hero_rusty_man)
        # print("spider_hero", hero_spider_man)

        hero_spider_man.team_id = team_preventer.id
        session.add(hero_spider_man)
        session.commit()
        session.refresh(hero_spider_man)


def select_heros():
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team, isouter=True)
        results = session.exec(statement)
        heros = results.all()
        print(heros)


def main():
    # create_db_and_tables()
    create_hero()
    # select_heros()
 

if __name__ == "__main__":
    main()