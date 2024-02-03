from typing import Optional

from sqlmodel import Field, SQLModel, create_engine, Session,select

DATA_BASE_URL="postgresql://saleemakhtar864:YUaiSR4gF5Bj@ep-bold-cell-01190632.us-east-2.aws.neon.tech/sql-tutorials?sslmode=require"





class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)




engine = create_engine(DATA_BASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Code above omitted 👆

def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)

        session.commit()


def update_hero():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.id == 1)
        results = session.exec(statement)

        hero_1 = results.one()
        print("-------------------------------")
        print("Before update; ", hero_1)

        hero_1.age = 45
        hero_1.name= "saram ali"
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)
        print("-------------------------------")

        print("After update; ", hero_1)


def delete_hero():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.id == 1)
        reults= session.exec(statement)
        hero_1 = reults.one()
        print("delete hero: ", hero_1)

        session.delete(hero_1)
        session.commit()
        session.refresh(hero_1)

        print("hereo deleted : ", hero_1)




def select_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.id == 1)
        results = session.exec(statement)
        print(results.first())


def main():
    # create_db_and_tables()
    # create_heroes()
    select_heroes()
    # update_hero()
    # delete_hero()

if __name__ == "__main__":
    main()