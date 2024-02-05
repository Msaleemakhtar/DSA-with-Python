from typing import Optional, List

from sqlmodel import Field, SQLModel, create_engine, Session,select, Relationship

from dotenv import load_dotenv, find_dotenv
from os import getenv




load_dotenv(find_dotenv())


Postgess_url = getenv("DATA_BASE_URL")

class HeroTeamLink(SQLModel, table=True):
    team_id: Optional[int] = Field(
        default=None, foreign_key="team.id", primary_key=True
    )
    hero_id: Optional[int] = Field(
        default=None, foreign_key="hero.id", primary_key=True
    )
    is_training: bool = False

    team: "Team" = Relationship(back_populates="hero_links")
    hero: "Hero" = Relationship(back_populates="team_links")

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str
    hero_links: List[HeroTeamLink] = Relationship(back_populates="team")
    
    

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    team_links: List[HeroTeamLink] = Relationship(back_populates="hero")
    


Postgess_url = getenv("DATA_BASE_URL")
engine = create_engine(Postgess_url, echo=True)

# Code above omitted 👆

def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
            teams=[team_z_force, team_preventers],
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            teams=[team_preventers],
        )
        hero_spider_boy = Hero(
            name="Spider-Boy", secret_name="Pedro Parqueador", teams=[team_preventers]
        )
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Deadpond:", hero_deadpond)
        print("Deadpond teams:", hero_deadpond.teams)
        print("Rusty-Man:", hero_rusty_man)
        print("Rusty-Man Teams:", hero_rusty_man.teams)
        print("Spider-Boy:", hero_spider_boy)
        print("Spider-Boy Teams:", hero_spider_boy.teams)

# Code below omitted 👇
# Code above omitted 👆

def update_heroes():
    with Session(engine) as session:
        hero_spider_boy = session.exec(
            select(Hero).where(Hero.name == "Spider-Boy")
        ).one()
        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

        hero_spider_boy.teams.remove(team_z_force)
        session.add(team_z_force)
        session.commit()

        print("Updated Spider-Boy's Teams:", hero_spider_boy.teams)
        print("Z-Force heroes:", team_z_force.heroes)

# Code below omitted 👇

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main():
 
  update_heroes()

if __name__ == "__main__":
    main()