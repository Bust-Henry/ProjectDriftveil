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
        
    def clearRegisteredPokemon(self):
        max = len(self.engine.execute(self.tab.select()).fetchall())
        for i in range(1, max+1):    
            self.engine.execute(self.tab.update().where(self.tab.c.nr==i).values(owned=0, shinyowned=0))

    def registerPokemon(self, number, shiny=False):
        try:
            if not shiny:
                result = self.engine.execute(self.tab.select().where(self.tab.c.nr==number)).fetchone()
                if result == None:
                    print("pokemon nr. " + number + " doesnt exists in this database")
                    return False
                currentlyowned = result[3]
                self.engine.execute(self.tab.update().where(self.tab.c.nr==number).values(owned=currentlyowned+1))
                return True
            else:
                result = self.engine.execute(self.tab.select().where(self.tab.c.nr==number)).fetchone()
                if result == None:
                    print("pokemon nr. " + number + " doesnt exists in this database")
                    return False
                currentlyowned = result[4]
                self.engine.execute(self.tab.update().where(self.tab.c.nr==number).values(shinyowned=currentlyowned+1))
                return True
        except IntegrityError:
            print("IntegrityError")
        return False

    def deRegisterPokemon(self, number, shiny=False):
        try:
            if not shiny:
                result = self.engine.execute(self.tab.select().where(self.tab.c.nr==number)).fetchone()
                if result == None:
                    print("pokemon nr. " + number + " doesnt exists in this database")
                    return False
                currentlyowned = result[3]
                newOwned = currentlyowned - 1
                if newOwned < 0:
                    newOwned = 0
                self.engine.execute(self.tab.update().where(self.tab.c.nr==number).values(owned=newOwned))
                return True
            else:
                result = self.engine.execute(self.tab.select().where(self.tab.c.nr==number)).fetchone()
                if result == None:
                    print("pokemon nr. " + number + " doesnt exists in this database")
                    return False
                currentlyowned = result[4]
                newOwned = currentlyowned - 1
                if newOwned < 0:
                    newOwned = 0
                self.engine.execute(self.tab.update().where(self.tab.c.nr==number).values(shinyowned=newOwned))
                return True
        except IntegrityError:
            print("IntegrityError")
        return False

    def getNextPokemon(self, shiny = False):
        if not shiny:
            result = self.engine.execute(self.tab.select().where(self.tab.c.owned==0)).fetchone()
        else:
            result = self.engine.execute(self.tab.select().where(self.tab.c.shinyowned==0)).fetchone()
        if not result:
            return None
        else:
            return result[2]
    
    def updateDatabase(self, pokemonlist:list):
        self.clearRegisteredPokemon()
        amount = 0
        for pokemon in pokemonlist:
            no = int.from_bytes(pokemon["monsno"], 'little', signed=False)
            colorno = int.from_bytes(pokemon["colorNo"], 'little', signed=False)
            if colorno == 0:
                shiny = False
            else:
                shiny = True
            self.registerPokemon(no, shiny)
            amount+=1
        print(amount, "pokemon added to the database!")