from typing import Optional, List

from sqlmodel import Field, SQLModel, create_engine, Session,select, Relationship

from dotenv import load_dotenv, find_dotenv
from os import getenv




load_dotenv(find_dotenv())


postgres_url = getenv("DATA_BASE_URL")



engine = create_engine(postgres_url, echo=True) 

# Code above omitted 👆

