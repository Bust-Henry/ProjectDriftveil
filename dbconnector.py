from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base
import os
# declarative base class
Base = declarative_base()

# Pokemon Table
class Pokemon(Base):
    __tablename__ = "pokemon"
    id = Column(Integer, primary_key=True)
    nr = Column(Integer, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    owned = Column(Integer, nullable=False)
    shinyowned = Column(Integer, nullable=False)

# Pokemon Element
class PokemonElement():
    def __init__(self, nr, name, owned, shinyowned):
        self.nr = nr
        self.name = name
        self.owned = owned
        self.shinyowned = shinyowned
    
    def toString(self):
        return str(self.nr) + ", " + self.name

class DBConnector:
    def __init__(self, dbpath) -> None:
        self.engine = create_engine('sqlite:///' + dbpath, echo=False)
        self.tab = Base.metadata.tables[Pokemon.__tablename__]

    def createDB(self):
        Pokemon.__table__.create(bind=self.engine, checkfirst=True)
    
    def add(self, pokemon:PokemonElement):
        try:
            self.engine.execute(self.tab.insert(), nr=pokemon.nr, name=pokemon.name, owned=pokemon.owned, shinyowned=pokemon.shinyowned)
        except IntegrityError:
            print(pokemon.toString(), "already exists. Skipping...")
